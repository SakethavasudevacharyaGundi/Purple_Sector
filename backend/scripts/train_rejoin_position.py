from pathlib import Path

from ml.traffic.rejoin_position_trainer import (
    RejoinPositionTrainer,
)


def main():

    trainer = (
        RejoinPositionTrainer()
    )

    (
        model,
        mae,
        _,
        _,
        _,
    ) = trainer.train(
        "data/ml/v1/rejoin_dataset.parquet"
    )

    model_dir = Path(
        "data/ml/models"
    )

    model_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    model_path = (
        model_dir
        /
        "rejoin_position_model.cbm"
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