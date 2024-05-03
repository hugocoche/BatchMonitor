"""
Description: This file contains the functions used in the streamlit app to create the database and the batch list from the data.

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
