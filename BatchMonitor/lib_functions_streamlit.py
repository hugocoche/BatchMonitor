"""Description

This file contains the functions used in the streamlit app to create the database and the batch list from the data.
"""

import pandas as pd
from BatchMonitor import BatchCollection, BatchLists, Item_in_batch, Batch


def createDatabaseFromBatchLists(data: BatchLists) -> pd.DataFrame:
    """Function allowing to create a database from the data. From the Batchlists class"""

    data_dict = {}
    for batches in data.batchlists:
        for batch in batches.batch_list:
            data_dict[batches.seller + "_" + batch.name] = {
                **{item.name: item.quantity_in_batch for item in batch.items},
                "Total": batch.price,
            }

    df = pd.DataFrame(data_dict)

    return df


def create_df_from_json(json_df: pd.DataFrame) -> pd.DataFrame:
    """Function allowing to create a database from the data. From the Batchlists class"""

    all_batch_with_seller = dict()
    quantities_of_items: dict[str, list[int | float]] = dict()

    for row in json_df.itertuples():
        batch_list = getattr(row, "batch_list")
        seller = getattr(row, "seller")
        all_batch_with_seller[seller] = {
            batch["name"]: batch["price"] for batch in batch_list
        }
        for batch in batch_list:
            for item in batch["items"]:
                item_name = item["name"]
                if item_name in quantities_of_items:
                    quantities_of_items[item_name].append(item["quantity_in_batch"])
                else:
                    quantities_of_items[item_name] = [item["quantity_in_batch"]]

    all_seller_with_doublons = [
        batch_seller
        for batch_seller in all_batch_with_seller
        for _ in all_batch_with_seller[batch_seller]
    ]

    all_batch = [
        batch
        for batch_seller in all_batch_with_seller
        for batch in all_batch_with_seller[batch_seller]
    ]

    unique_batch = []
    for i, batch in enumerate(all_batch):
        counter = all_batch.count(batch)
        if batch in unique_batch:
            all_batch[i] = batch + f".{counter}"
            counter += 1
        unique_batch.append(all_batch[i])

    all_price = [
        all_batch_with_seller[batch_seller][batch]
        for batch_seller in all_batch_with_seller
        for batch in all_batch_with_seller[batch_seller]
    ]

    already_seen = set()
    all_item_name = []
    for batches in json_df["batch_list"]:
        for batch in batches:
            for item in batch["items"]:
                if item["name"] not in already_seen:
                    all_item_name.append(item["name"])
                    already_seen.add(item["name"])
    all_item_name.append("TOTAL")
    all_item_name.append("Seller")

    df = pd.DataFrame(data=json_df, columns=all_batch, index=all_item_name)

    for row_item in quantities_of_items.keys():
        df.loc[row_item] = quantities_of_items[row_item]
    df.loc["TOTAL"] = all_price
    df = df.astype(object)
    df.loc["Seller"] = all_seller_with_doublons

    return df


def indice_batch_current_seller(Batches: BatchLists, seller) -> int | None:
    if Batches is not None and seller is not None:
        for i, batchcollection in enumerate(Batches.batchlists):
            if batchcollection.seller == seller:
                index = i
                break
        return index
    return None


def batch_list_global(database):
    batches = None
    already_seen = []
    for batchSeller_name, Batch_Value in zip(database.columns, database.iloc[-1]):
        items = [
            Item_in_batch(Item_Name, Item_Value)
            for Item_Name, Item_Value in zip(
                database.index[:-1], database[batchSeller_name][:-1]
            )
        ]
        if batches is None:
            batches = BatchLists(
                batchlists=[
                    BatchCollection(
                        batch_list=[
                            Batch(
                                batchSeller_name,
                                Batch_Value,
                                items,
                            )
                        ],
                        seller="All",
                    )
                ]
            )
            already_seen.append(batchSeller_name)
        else:
            if batchSeller_name not in already_seen:
                for batchcollection in batches:
                    batchcollection.batch_list.append(
                        Batch(
                            batchSeller_name,
                            Batch_Value,
                            items,
                        )
                    )
                already_seen.append(batchSeller_name)
            else:
                for batchcollection in batches.batchlists:
                    if batchcollection.seller == batchSeller_name:
                        batchcollection.batch_list.items.append(items)

    return batches
