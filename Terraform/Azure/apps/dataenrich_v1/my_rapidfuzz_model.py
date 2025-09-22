import gc
import os
import pandas as pd
from io import BytesIO
from azure.storage.blob import BlobServiceClient

import pandas as pd
from tqdm import tqdm
from rapidfuzz import fuzz, process, utils
from joblib import Parallel, delayed
from multiprocessing import cpu_count
from typing import List, Tuple, Callable, Union


class RapidFuzz:

    """
    A class for efficient fuzzy string matching using RapidFuzz library.

    This class provides methods for calculating edit distances between lists of strings
    using various scoring algorithms from the RapidFuzz library. It supports parallel
    processing for improved performance on large datasets.

    Attributes:
        n_jobs (int): Number of parallel processes to use. -1 uses all available CPU cores.
        score_cutoff (float): Minimum similarity threshold (0 to 1) for considering a match.
        scorer (Callable): The scoring function to use for calculating string similarity.
        equal_lists (bool): Internal flag to optimize matching when comparing a list to itself.

    Args:
        n_jobs (int, optional): Number of parallel processes. Defaults to -1 (all cores).
        score_cutoff (float, optional): Minimum similarity threshold. Defaults to 0.
        scorer (Callable, optional): Scoring function. Defaults to fuzz.token_set_ratio.

    Available Scorers:
        - fuzz.ratio: Simple ratio between two strings
        - fuzz.partial_ratio: Best partial ratio between two strings
        - fuzz.token_sort_ratio: Ratio of sorted token strings
        - fuzz.partial_token_sort_ratio: Partial ratio of sorted token strings
        - fuzz.token_set_ratio: Ratio of token sets
        - fuzz.partial_token_set_ratio: Partial ratio of token sets
        - fuzz.token_ratio: Best ratio of token strings
        - fuzz.partial_token_ratio: Best partial ratio of token strings
        - fuzz.WRatio: Weighted ratio of multiple scoring algorithms
        - fuzz.QRatio: Quick ratio for fast string matching

    Example:
        fuzzy_matcher = RapidFuzz(n_jobs=-1, score_cutoff=0.8, scorer=fuzz.WRatio)
        matches = fuzzy_matcher.match(['apple', 'banana'], ['appl', 'orange', 'bananas'])
    """

    def __init__(self, n_jobs: int = -1, score_cutoff: float = 0, scorer: Callable = fuzz.token_set_ratio):
        
        self.score_cutoff = score_cutoff * 100
        self.scorer = scorer
        self.equal_lists = False

        if n_jobs == -1:
            self.n_jobs = cpu_count()
        else:
            self.n_jobs = n_jobs

    

    def _calculate_edit_distance_one(self, from_string: str, to_list: List[str]) -> Tuple[str, Union[str, None], float]:
        """
            Internal method to find the best single match for a string.
            
            Args:
                from_string (str): The string to match.
                to_list (List[str]): The list of strings to match against.
            
            Returns:
                Tuple[str, Union[str, None], float]: (original string, best match or None, similarity score)
        """
        if self.equal_lists:
            to_list.remove(from_string)

        match = process.extractOne(from_string, to_list, score_cutoff=self.score_cutoff, scorer=self.scorer)

        if match:
            return from_string, match[0], match[1] / 100
        else:
            return from_string, None, 0.



    def matchOne(self, from_list: List[str], to_list: List[str] = None) -> pd.DataFrame:

        """
        Calculate the best single match for each string in from_list against to_list.

        This method finds the best matching string in to_list for each string in from_list,
        using the configured scorer and similarity threshold.

        Args:
            from_list (List[str]): The source list of strings to match from.
            to_list (List[str], optional): The target list to match against. If None,
                matches within from_list. Defaults to None.

        Returns:
            pd.DataFrame: A DataFrame containing match results with columns:
                - 'From': Original string from from_list
                - 'To': Best matching string from to_list (or None if no match)
                - 'Similarity': Similarity score (0 to 1)

        Example:
            matcher = RapidFuzz(score_cutoff=0.8)
            result = matcher.matchOne(['apple', 'banana'], ['appl', 'bananas'])
            print(result)
            From     To         Similarity
            0  apple    appl       0.89
            1  banana   bananas    0.92
        
        Notes:
            - If to_list is None, the method will match within from_list (excluding self-matches)
            - Parallel processing is used for improved performance
        """
        
        if to_list is None:
            self.equal_lists = True
            expected_iterations = int(len(from_list)/2)
            to_list = from_list.copy()
        else:
            expected_iterations = len(from_list)

        matches = Parallel(n_jobs=self.n_jobs)(delayed(self._calculate_edit_distance_one)
                                                (from_string, to_list)
                                                for from_string in tqdm(from_list, total=expected_iterations,
                                                                        disable=True))
        matches = pd.DataFrame(matches, columns=['From', "To", "Similarity"])
        return matches
    



    def _calculate_edit_distance(self, from_string: str, to_list: List[str]) -> List[Tuple[str, Union[str, None], float]]:
        """
        Internal method to find all matches for a string above the score cutoff.
        
        Args:
            from_string (str): The string to match.
            to_list (List[str]): The list of strings to match against.
        
        Returns:
            List[Tuple[str, Union[str, None], float]]: List of (original string, match or None, similarity score)
        """
        if self.equal_lists:
            to_list = [item for item in to_list if item != from_string]

        if not to_list:  # Handle empty to_list case
            return [(from_string, None, 0)]

        matches = process.extract(from_string, to_list, limit=None, scorer=self.scorer, score_cutoff=self.score_cutoff)
        # Filter matches by score_cutoff and convert the score to a decimal
        matches = [(from_string, match[0], match[1] / 100) for match in matches]
        # matches = [(from_string, match[0], match[1] / 100) for match in matches if match[1] >= self.score_cutoff * 100]

        if not matches:  # Handle no matches found
            return [(from_string, None, 0)]

        return matches
    


    def match(self, from_list: List[str], to_list: List[str] = None) -> pd.DataFrame:
        """
        Calculate all possible matches between from_list and to_list above the score cutoff.

        This method finds all matching strings in to_list for each string in from_list
        that meet or exceed the configured similarity threshold.

        Args:
            from_list (List[str]): The source list of strings to match from.
            to_list (List[str], optional): The target list to match against. If None,
                matches within from_list. Defaults to None.

        Returns:
            pd.DataFrame: A DataFrame containing all match results with columns:
                - 'From': Original string from from_list
                - 'To': Matching string from to_list (or None if no match)
                - 'Similarity': Similarity score (0 to 1)

        Example:
            matcher = RapidFuzz(score_cutoff=0.8)
            result = matcher.match(['apple', 'banana'], ['appl', 'aple', 'bananas'])
            print(result)
            From     To         Similarity
            0  apple    appl       0.89
            1  apple    aple       0.84
            2  banana   bananas    0.92
        
        Notes:
            - If to_list is None, the method will match within from_list (excluding self-matches)
            - Returns multiple matches per string if they meet the similarity threshold
            - Parallel processing is used for improved performance
            - No matches will return a row with None in the 'To' column and 0 similarity
        """
        if to_list is None:
            self.equal_lists = True
            to_list = from_list.copy()
        else:
            self.equal_lists = False

        # Run the matching in parallel
        results = Parallel(n_jobs=self.n_jobs)(
            delayed(self._calculate_edit_distance)(from_string, to_list) for from_string in tqdm(from_list, disable=True)
        )

        matches = [item for sublist in results for item in sublist]
        matches = pd.DataFrame(matches, columns=['From', 'To', 'Similarity'])
        # Flatten the list of lists into a single list of tuples
        return matches



def get_blob():

    # Load connection string from environment
    conn_str = os.getenv("AzureWebJobsStorage")
    container_name = "parquet-files"
    blob_name = "titanic.parquet"

    # Connect to blob storage
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    # Download blob as byte stream
    stream_downloader = blob_client.download_blob()
    blob_data = BytesIO(stream_downloader.readall())

    return blob_data



if __name__ == "__main__":

    print("I am here....")

    blob_data = get_blob()

    # Load into DataFrame
    df_to_process = pd.read_parquet(blob_data)

    # Preview
    print(f"df_to_process.shape:{df_to_process.shape}")
    print(df_to_process.head())

    ###########################
    ##### RAPIDFUZZ MODEL #####
    ###########################
    print("Search module launched")
    model = RapidFuzz(scorer=fuzz.token_set_ratio, score_cutoff=0.6) 

    #unique_name = df_to_process.select('name').unique().to_series().to_list()
    unique_name = df_to_process['Name'].unique().tolist()


    for item in unique_name[:200]:
        print(item)


    if not unique_name:
        print("No name available for matching")

    print(f"len(unique_name):{len(unique_name)}")

    search_string = "John"

    match_result = model.match([search_string.strip()], unique_name) # The inputs should be in list format
    print("Customer search finished")

    # match_result = pl.DataFrame(match_result)[['To', 'Similarity']]\
    # .with_columns(
    #     [pl.col('Similarity').round(3)]
    #     )
    

    # Convert to DataFrame and select columns
    df_match = pd.DataFrame(match_result)[['To', 'Similarity']]

    # Round the Similarity column to 3 decimal places
    df_match['Similarity'] = df_match['Similarity'].round(3)

    print(f"df_match.shape: {df_match.shape}")

    print(f"df_match.head: {df_match.head(10)}")

    del unique_name
    gc.collect()

    # result_df = df_to_process.filter(
    #     pl.col('JoinedAddress').is_in(match_result['To'].to_list())
    #     ).select(params.FINAL_COLS).unique()

    # Filter rows where 'JoinedAddress' is in match_result['To']
    filtered_df = df_to_process[df_to_process['Name'].isin(match_result['To'].tolist())]


    FINAL_COLS = ['PassengerId', 'Survived', 'Name', 'Sex', 'Ticket']

    # Select final columns and drop duplicates
    result_df = filtered_df[FINAL_COLS].drop_duplicates()

    print(f"result_df.shape: {result_df.shape}")

    print(f"result_df.head(20):{result_df.head(20)}")


    # # Join the result DataFrame with match results on 'JoinedAddress' and 'To' columns
    # # Then, drop the 'JoinedAddress' column from the final result and ensure uniqueness
    # result_df = result_df.join(match_result, left_on='JoinedAddress', right_on='To').drop(['JoinedAddress']).unique()

    # Join on JoinedAddress and To
    merged_df = result_df.merge(match_result, left_on='Name', right_on='To')

    # Drop redundant column
    merged_df.drop(columns=['Name'], inplace=True)

    # Remove duplicates
    result_df = merged_df.drop_duplicates()

    print(f"result_df.shape: {result_df.shape}")

    print(f"result_df.head(20):{result_df.head(20)}")

    
