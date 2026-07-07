from pathlib import Path

from ml.pitloss.pitloss_trainer import (
    PitLossTrainer,
)


def main():

    trainer = (
        PitLossTrainer()
    )

    (
        model,
        mae,
        X_test,
        y_test,
        predictions,
    ) = trainer.train(
        "data/ml/v1/pit_loss_dataset.parquet"
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
        "pit_loss_model.cbm"
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