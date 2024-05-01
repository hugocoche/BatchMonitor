"""
Description: This file contains the functions used in the streamlit app to create the database and the batch list from the data.

"""
import pandas as pd
from batches_optimization import  BatchCollection, BatchLists, Item_in_batch, Batch


def createDatabaseFromBatchLists(data: BatchLists) -> pd.DataFrame:
    """Function allowing to create a database from the data. From the Batchlists class"""

    new_data = data
    for i in range(len(new_data.batchlists)):
        for j in range(len(new_data.batchlists[i].batch_list)):
            temp_dict = {
                item.name: item.quantity_in_batch
                for item in new_data.batchlists[i].batch_list[j].items
            }
            new_data.batchlists[i].batch_list[j].items = temp_dict

    for i in range(len(new_data.batchlists)):
        for j in range(len(new_data.batchlists[i].batch_list)):
            new_data.batchlists[i].batch_list[j].items = dict(
                sorted(new_data.batchlists[i].batch_list[j].items.items())
            )

    numeraire = []
    for batches in new_data.batchlists:
        for batch in batches.batch_list:
            row = list(batch.items.values())
            row.append(batch.price)
            numeraire.append(row)

    items = set()
    for batches in new_data.batchlists:
        for batch in batches.batch_list:
            items.update(batch.items.keys())
    items = sorted(list(items))
    items.append("Total")

    list_of_batches = []
    for batches in new_data.batchlists:
        for batch in batches.batch_list:
            batch_name = batches.seller + "_" + batch.name
            list_of_batches.append(str(batch_name))

    df = pd.DataFrame(numeraire, columns=items, index=list_of_batches)

    return df.transpose()

def indice_batch_current_seller(Batches: BatchLists, seller) -> int:
    if Batches is not None and seller is not None:
        for i, batchcollection in enumerate(Batches.batchlists):
            if batchcollection.seller == seller:
                index = i
                break

        return index

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
                        batchcollection.batch_list.items.extend(items)

    return batches