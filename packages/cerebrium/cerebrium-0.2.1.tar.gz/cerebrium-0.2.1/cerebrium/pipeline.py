from pipeline import Pipeline
from typing import Tuple, List
from enum import Enum


class ModelType(Enum):
    XGBOOST_CLASSIFIER = "xgboost_classifier"
    XGBOOST_REGRESSOR = "xgboost_regressor"
    TORCH = "torch"
    SKLEARN = "sklearn"
    SKLEARN_CLASSIFIER = "sklearn_classifier"
    ONNX = "onnx"


CerebriumPipeline = List[Tuple[ModelType, str]]


def _check_pipeline_type(model_pipeline: any) -> CerebriumPipeline:
    """
    Check if the given model_pipeline is a valid CerebriumPipeline.

    Args:
        model_pipeline: The model_pipeline to check.

    Raises:
        TypeError: If the model_pipeline is not a valid CerebriumPipeline.
    """
    if not isinstance(model_pipeline, list) and not isinstance(model_pipeline, tuple):
        raise TypeError(
            f"model_pipeline must be a tuple or list, but is {type(model_pipeline)}"
        )
    if len(model_pipeline) == 2:
        if (
            not isinstance(model_pipeline[0], list)
            and not isinstance(model_pipeline[0], tuple)
            and not isinstance(model_pipeline[1], list)
            and not isinstance(model_pipeline[1], tuple)
        ):
            model_pipeline = [model_pipeline]

    for i, (model_type, model_filepath) in enumerate(model_pipeline):
        if i > 0 and model_type == ModelType.ONNX:
            raise NotImplementedError(
                "ONNX models are currently only supported as initial models in pipelines."
            )
        if not isinstance(model_type, ModelType):
            raise TypeError(
                f"Model {i}: model_type must be of type ModelType, but is {type(model_type)}. Please ensure you use a valid Cerebrium typing."
            )
        if not isinstance(model_filepath, str):
            raise TypeError(
                f"Model {i}: model_filepath must be of type str, but is {type(model_filepath)}"
            )
        else:
            if (
                not model_filepath.endswith(".pkl")
                and not model_filepath.endswith(".pt")
                and not model_filepath.endswith(".json")
                and not model_filepath.endswith(".onnx")
            ):
                raise TypeError(
                    f"Model {i}: model_filepath must be be a valid file type, but is {model_filepath}"
                )
    return model_pipeline


def _generate_pipeline(pipeline_name: str, pipeline: CerebriumPipeline) -> Pipeline:
    """
    Generate a Pipeline for the given CerebriumPipeline.

    Args:
        pipeline_name (str): The name of the pipeline.
        model_pipeline: The CerebriumPipeline to generate a Pipeline for.

    Returns:
        Pipeline: The generated pipeline.
    """
    pipeline_string = (
        "from pipeline import Pipeline, Variable, PipelineFile\n"
        "from cerebrium.models.pickle import PickleModel, PickleClassifierModel\n"
        "from cerebrium.models.torch import TorchModel, TorchPickleModel\n"
        "from cerebrium.models.xgboost import XGBClassifierModel, XGBRegressorModel\n"
        "from cerebrium.models.onnx import OnnxModel\n"
        f"with Pipeline('{pipeline_name}') as pipeline:\n"
        "    input_list = Variable(type_class="
        "dict, is_input=True)\n" if pipeline[0][0] == ModelType.ONNX else  "list, is_input=True)\n"
    )
    for i, (_, model_filepath) in enumerate(pipeline):
        pipeline_string += (
            f"    model_file_{i} = PipelineFile(path='./{model_filepath}')\n"
        )

    pipeline_string += "    pipeline.add_variables(input_list,"
    for i in range(len(pipeline)):
        pipeline_string += f"model_file_{i},"
    pipeline_string += ")\n"

    for i, (model_type, model_filepath) in enumerate(pipeline):
        if model_filepath.endswith(".pkl"):
            if model_type == ModelType.TORCH:
                pipeline_string += f"    model_{i} = TorchPickleModel()\n"
            elif (
                model_type == ModelType.XGBOOST_CLASSIFIER
                or model_type == ModelType.SKLEARN_CLASSIFIER
            ):
                pipeline_string += f"    model_{i} = ClassifierPickleModel()\n"
            else:
                pipeline_string += f"    model_{i} = PickleModel()\n"
        elif model_type == ModelType.XGBOOST_CLASSIFIER:
            pipeline_string += f"    model_{i} = XGBClassifierModel()\n"
        elif model_type == ModelType.XGBOOST_REGRESSOR:
            pipeline_string += f"    model_{i} = XGBRegressorModel()\n"
        elif model_type == ModelType.TORCH:
            pipeline_string += f"    model_{i} = TorchModel()\n"
        elif model_type == ModelType.ONNX:
            pipeline_string += f"    model_{i} = OnnxModel()\n"

        pipeline_string += f"    model_{i}.load(model_file_{i})\n"

    if pipeline[0][1] == ModelType.ONNX:
        pipeline_string += f"    output_0 = model_0.predict(output_{i-1})['output']\n"
    else:
        pipeline_string += "    output_0 = model_0.predict(input_list)\n"
    for i in range(1, len(pipeline)):
        if (
            pipeline[i][1] == ModelType.SKLEARN_CLASSIFIER
            or pipeline[i][1] == ModelType.XGBOOST_CLASSIFIER
        ):
            pipeline_string += (
                f"    output_{i} = model_{i}.predict_proba(output_{i-1})\n"
            )
        else:
            pipeline_string += f"    output_{i} = model_{i}.predict(output_{i-1})\n"
    pipeline_string += f"    pipeline.output(output_{len(pipeline)-1})\n"
    exec(pipeline_string)
    return Pipeline.get_pipeline(pipeline_name)
