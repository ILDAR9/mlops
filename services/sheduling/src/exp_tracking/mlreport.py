import json
import logging
import os
from pathlib import Path
from typing import List, Dict

import mlflow
import pandas as pd
from mlflow.entities import ViewType

logger = logging.getLogger(__name__)

is_mlflow_ready = False

KEY_EXP_NAME = "EXPERIMENT_NAME"


def _prepare_mlflow() -> None:
    global is_mlflow_ready
    if is_mlflow_ready:
        return
    cfg_path = Path(__file__).parent.as_posix() + '/config.json'
    with open(cfg_path) as f:
        cfg = json.load(f)['mlflow']

    os.environ["AWS_ACCESS_KEY_ID"] = cfg['AWS_ACCESS_KEY_ID']
    os.environ["AWS_SECRET_ACCESS_KEY"] = cfg['AWS_SECRET_ACCESS_KEY']
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = cfg['MLFLOW_S3_ENDPOINT_URL']
    if KEY_EXP_NAME not in os.environ:
        os.environ[KEY_EXP_NAME] = cfg['default_experiment_name']
    mlflow.set_tracking_uri(cfg['MLFLOW_TRACKING_URL'])
    is_mlflow_ready = True
    logger.debug("Mlflow client is initialized")


def get_candidate_run_names(run_names: List[str]) -> List[str]:
    _prepare_mlflow()
    candidates = []
    experiment_name = os.environ[KEY_EXP_NAME]
    for name in run_names:
        res = mlflow.search_runs(experiment_names=[experiment_name],
                                 filter_string=f"tags.mlflow.runName = '{name}'",
                                 run_view_type=ViewType.ACTIVE_ONLY, max_results=1, output_format='list')
        if not bool(res):
            candidates.append(name)
    return candidates


def log_experiment_run(run_info: Dict):
    _prepare_mlflow()
    experiment_name = os.environ[KEY_EXP_NAME]
    try:
        experiment_id = mlflow.create_experiment(name=experiment_name)
    except:
        experiment_id = mlflow.get_experiment_by_name(name=experiment_name).experiment_id

    run_name: str = run_info['run_name']
    # version = re.search(r'v(\d+)', run_name).group(1)
    # version = int(version)
    logger.debug(f"Start dumping run-info for mlflow.runName='{run_name}'")
    with mlflow.start_run(experiment_id=experiment_id, run_name=run_name):
        # Params & Tags
        mlflow.log_params(run_info['params'])
        mlflow.set_tags(run_info['tags'])

        # Artefacts
        for fpath in run_info['artifacts']:
            mlflow.log_artifact(fpath)

        # Global metrics
        mlflow.log_metrics(run_info['metrics'])

        # Metrics timeseries
        train_records = run_info['train_records']
        df_eval = pd.DataFrame.from_records(filter(lambda d: d['phase'] == 'evaluation', train_records))
        df_eval = df_eval.groupby(['episode'])['completion_percentage'].mean()

        for d in filter(lambda d: d['phase'] == 'training', train_records):
            episode = int(d['episode'])
            mlflow.log_metric(key="completion_percentage", value=d['completion_percentage'], step=episode)
            mlflow.log_metric(key="reward_score", value=d['reward_score'], step=episode)
            if episode in df_eval:
                mlflow.log_metric(key='avg_eval_completion_percentage', value=df_eval[episode], step=episode)
    logger.info(f"Dumped run-info for mlflow.runName='{run_name}'")
