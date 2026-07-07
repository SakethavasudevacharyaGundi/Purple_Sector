from ml.datasets.production_dataset_builder import (
    ProductionDatasetBuilder,
)


def main():

    builder = (
        ProductionDatasetBuilder()
    )

    df = builder.build(
        start_year=2023,
        end_year=2023,
    )

    print()

    print(
        "FINAL DATASET SHAPE"
    )

    print(
        df.shape
    )

    print()

    print(
        df.head()
    )


if __name__ == "__main__":
    main()