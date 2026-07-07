from pathlib import Path

from ml.pace.pace_trainer import (
    PaceTrainer,
)


def main():

    trainer = (
        PaceTrainer()
    )

    (
        model,
        mae,
        X_test,
        y_test,
        predictions,
    ) = trainer.train(
        "data/ml/v1/pace_dataset.parquet"
    )

    model_dir = Path(
        "data/ml/models"
    )

    model_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    model_path = (
        model_dir /
        "pace_model.cbm"
    )

    model.save_model(
        model_path
    )

    print()

    print(
        f"Final MAE: {mae:.4f}"
    )

    print(
        f"Saved: {model_path}"
    )


if __name__ == "__main__":
    main()