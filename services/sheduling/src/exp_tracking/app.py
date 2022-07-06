import logging
import os
from typing import Dict, List

import pandas as pd

from exp_tracking import mlreport, load_data, convert_delta_ms, convert_delta_ms_hours
from utils import TMP_FLD
from utils import s3control as s3

logger = logging.getLogger(__name__)


def _prepare_test_artifacts(eval_d: Dict, model_name: str) -> str:
    df = pd.DataFrame.from_records(eval_d)

    df['Time (MM:ss:mmm)'] = df['elapsed_time_in_milliseconds'].apply(convert_delta_ms)
    columns = ['trial', 'Time (MM:ss:mmm)', 'completion_percentage', 'episode_status']
    df = df[columns]
    df.rename(columns={'trial': 'Trial',
                       'completion_percentage': '% track completed',
                       'episode_status': 'Status'}, inplace=True)
    eval_html_fpath = os.path.join(TMP_FLD, model_name, 'eval_metrics.html')
    df.to_html(eval_html_fpath)
    return eval_html_fpath


def prepare_run_info(model_name: str) -> Dict:
    try:
        eval_fpath = s3.load_file(model_name, 'EvaluationMetrics.json')
    except s3.S3NotFoundError:
        logger.warning(f"No 'EvaluationMetrics.json' for '{model_name}'")
        eval_fpath = None

    # Mandatory
    train_fpath = s3.load_file(model_name, 'TrainingMetrics.json')
    trparams_fpath = s3.load_file(model_name, 'training_params.yaml')
    metadata_fpath = s3.load_file(model_name, 'model/model_metadata.json')
    hyper_fpath = s3.load_file(model_name, 'ip/hyperparameters.json')
    reward_fpath = s3.load_file(model_name, 'reward_function.py')

    artifacts = [reward_fpath]

    # Optional
    try:
        video_topview_fpath = s3.load_file(model_name, 'camera-topview-video.mp4')
        video_pip_fpath = s3.load_file(model_name, 'camera-pip-video.mp4')
        artifacts += [video_topview_fpath, video_pip_fpath]
    except s3.S3NotFoundError:
        logger.warning(f"No mp4 files for '{model_name}'")


    # Load data
    train_records = load_data(train_fpath)['metrics']
    params_d = load_data(trparams_fpath)
    meta_d = load_data(metadata_fpath)
    hyper_d = load_data(hyper_fpath)

    # Prepare run info for Train
    total_time_in_ms = sum(map(int, (d['elapsed_time_in_milliseconds'] for d in train_records)))
    train_duration = convert_delta_ms_hours(total_time_in_ms)

    params = dict(
        speed_high=meta_d['action_space']['speed']['high'],
        speed_low=meta_d['action_space']['speed']['low'],
        algorithm=meta_d['training_algorithm'],
        train_duration=train_duration
    )
    params.update(hyper_d)

    tags = dict(
        sensor='/'.join(meta_d['sensor']),
        race_type=params_d['RACE_TYPE'],
        track=params_d['WORLD_NAME'],
        change_start_position=params_d['CHANGE_START_POSITION']
    )

    # Prepare run info for Test
    if eval_fpath:
        eval_d = load_data(eval_fpath)['metrics']
        df = pd.DataFrame.from_records(eval_d)
        metrics = dict(
            test_completion_pecentage=df.completion_percentage.mean(),
            test_track_time=df.elapsed_time_in_milliseconds.mean()
        )

        eval_html_fpath = _prepare_test_artifacts(eval_d, model_name)
        artifacts.append(eval_html_fpath)

        del df, eval_d
    else:
        metrics = dict()

    return dict(
        run_name=model_name,
        params=params, tags=tags, metrics=metrics, artifacts=artifacts,
        train_records=train_records
    )


def reveal_new_models() -> List[str]:
    all_model_names = s3.get_model_buckets()
    if not all_model_names:
        return []
    model_name_buckets = mlreport.get_candidate_run_names(all_model_names)
    logger.info(f"Candidates for tracking: {model_name_buckets}")
    return model_name_buckets


def process(model_name_list: List[str]) -> None:
    for i, model_name in enumerate(model_name_list, 1):
        run_info = prepare_run_info(model_name)
        mlreport.log_experiment_run(run_info)
        logger.info(f"{i}) Finished tracking '{model_name}'.")


if __name__ == '__main__':
    candidates = reveal_new_models()
    process(candidates)
