import argparse
from transformers import AutoModelForCausalLM
from lighteval.logging.evaluation_tracker import EvaluationTracker
from lighteval.models.transformers.transformers_model import TransformersModel, TransformersModelConfig
from lighteval.pipeline import ParallelismManager, Pipeline, PipelineParameters
from lighteval.utils.imports import is_package_available

MODEL_NAME = "Qwen/Qwen3.5-0.8B" # Qwen/Qwen3.5-4B
# Kiti matematiniai, loginiai, bendrojo išprusimo benchmarkai: aime25, math, gsm8k
BENCHMARKS = "aime25" # You can specify multiple benchmarks by separating them with commas, e.g. "aime25,math,gsm8k"
MAX_SAMPLES = 1 # Maximum number of samples to evaluate per task. Set to None to evaluate all samples.
BATCH_SIZE = 1 # Inference batch size. Adjust based on your GPU memory. Set to 1 for no batching.

if is_package_available("accelerate"):
    from datetime import timedelta
    from accelerate import Accelerator, InitProcessGroupKwargs
    accelerator = Accelerator(kwargs_handlers=[InitProcessGroupKwargs(timeout=timedelta(seconds=3000))])
else:
    accelerator = None

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a LightEval benchmark with a Transformers model.")
    parser.add_argument("--model", default=MODEL_NAME, help="Hugging Face model name")
    parser.add_argument("--benchmark", default=BENCHMARKS, help="LightEval task(s), e.g. aime25")
    parser.add_argument("--max-samples", type=int, default=MAX_SAMPLES, help="Max samples per task")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Inference batch size")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    evaluation_tracker = EvaluationTracker(output_dir="./results")
    pipeline_params = PipelineParameters(
        launcher_type=ParallelismManager.ACCELERATE if accelerator is not None else ParallelismManager.NONE,
        max_samples=args.max_samples,
    )

    hf_model = AutoModelForCausalLM.from_pretrained(args.model, device_map="cuda:0")
    config = TransformersModelConfig(model_name=args.model, batch_size=args.batch_size, max_length=204800)
    model = TransformersModel.from_model(hf_model, config)

    pipeline = Pipeline(
        model=model,
        pipeline_parameters=pipeline_params,
        evaluation_tracker=evaluation_tracker,
        tasks=args.benchmark,
    )

    pipeline.evaluate()
    pipeline.show_results()
    pipeline.get_results()


if __name__ == "__main__":
    main()