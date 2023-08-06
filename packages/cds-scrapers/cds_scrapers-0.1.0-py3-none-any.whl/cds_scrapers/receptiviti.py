#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Created By  : Alberto Marengo
# Created Date: 10/24/22
# version ='0.1.0'
# ---------------------------------------------------------------------------
"""
This class takes a conversation pandas DataFrame, sends the data through Receptiviti API and
stores the enriched data into 10 interior pandas DataFrame:
1)  df_enriched_personality
2)  df_enriched_liwc
3)  df_enriched_time_orientation
4)  df_enriched_needs_values
5)  df_enriched_cognition
6)  df_enriched_social_dynamics
7)  df_enriched_drives
8)  df_enriched_emotions
9)  df_enriched_summary
10) df_enriched_taxonomies
"""
# ---------------------------------------------------------------------------

import pandas as pd
import json
import requests
import numpy as np
import textstat

class Receptiviti():
    """
    A class that takes a pandas DataFrame of a conversation as input, pass it through the Receptiviti API and returns the metrics. 
    It also calculates the readability using the textstat library (https://pypi.org/project/textstat/).
    
    Paramaters
    ----------
    agg_minutes: int
        The aggregation time in minutes. By default, the conversation is aggregated every 15 minutes
    time_aggregation: bool
        If you want to aggregate by time. Default is True. Pass False to get the metrics for the whole conversation
    grouped: bool
        If you want to group the speakers. Default is False. If True is passed you must pass the 'speaker' parameter as well
    speaker: str
        Pass the speaker you want to get the metric for. Accepted values are a speaker_id or 'all' if metrics for the whole group of speakers is needed

    Methods
    -------
    run
        This method manipulates the input DataFrame and creates 10 new DataFrames containing 230 metrics from Receptiviti in total.
    """


    def __init__(self, API_key: str, API_secret: str) -> None:
        self.RECEPTIVITI_URL = 'https://api.receptiviti.com/v1/framework'
        self.RECEPTIVITI_API_KEY = API_key
        self.RECEPTIVITI_API_SECRET = API_secret
        self.groups = {'personality': ['personality', 'disc_dimensions'],
                       'liwc': ['liwc','liwc_extension'],
                       'time_orientation': ['additional_indicators'],
                       'needs_values': ['needs', 'values'],
                       'cognition': ['cognition'],
                       'social_dynamics': ['social_dynamics'],
                       'drives': ['drives'],
                       'emotions': ['sallee'],
                       'summary': ['summary'],
                       'taxonomies': ['taxonomies'] } # grouped from receptiviti API call response
        self.df_enriched_personality = pd.DataFrame()
        self.df_enriched_liwc = pd.DataFrame()
        self.df_enriched_time_orientation = pd.DataFrame()
        self.df_enriched_needs_values = pd.DataFrame()
        self.df_enriched_cognition = pd.DataFrame()
        self.df_enriched_social_dynamics = pd.DataFrame()
        self.df_enriched_drives = pd.DataFrame()
        self.df_enriched_emotions = pd.DataFrame()
        self.df_enriched_summary = pd.DataFrame()
        self.df_enriched_taxonomies = pd.DataFrame()
    
    def run(self, df: pd.DataFrame, agg_minutes:int = 15, time_aggregation: bool = True, grouped: bool = False, speaker:str = None) -> None:
        """
        This method runs the data aggregation and pass it through the Receptiviti API

        Parameters
        ----------
        df: Pandas DataFrame
                Needs to have the following columns:
                - speaker_id
                - utterance
                - timestamp_start
                - timestamp_end
                - conversation_id (Optional)
        agg_minutes: int
            The aggregation time in minutes. By default, the conversation is aggregated every 15 minutes
        time_aggregation: bool
            If you want to aggregate by time. Default is True. Pass False to get the metrics for the whole conversation
        grouped: bool
            If you want to group the speakers. Default is False. If True is passed you must pass the 'speaker' parameter as well
        speaker: str
            Pass the speaker you want to get the metric for. Accepted values are a speaker_id or 'all' if metrics for the whole group of speakers is needed
        """
        self.df = df
        if 'conversation_id' in df.columns.tolist(): # Checks if there is a conversation_id column
            self.id_present = True
            if df['conversation_id'].nunique() == 1:
                self.conversation_id = df['conversation_id'].unique().tolist()[0]
            else:
                print('It looks like there is more than one conversation in this file')
        self.agg_minutes = agg_minutes
        self.time_aggregation = time_aggregation
        self.grouped = grouped
        self.speaker = speaker
        self._prepare_df()
        if self.time_aggregation: # returns metrics aggregated by time
            speakers, utterances, conv_group_range, readability_scores = self._group_df()
            results_API = dict()
            for idx, (speaker, utterance, conv_group) in enumerate(zip(speakers, utterances, conv_group_range)):
                request_id = ('00'+str(conv_group))[-4:] + "_" + str(speaker) # if time aggregation the id is combo of group time range and speaker_id
                data = json.dumps({'request_id': request_id, 'content': utterance})
                resp = self._call_API(data)
                results_API[request_id] = resp.json() # adds results to the dictionary for the key request_id
                results_API[request_id]['readability'] = readability_scores[idx]
        else: # returns metrics for the whole conversation
            speakers, utterances, readability_scores = self._group_df()
            results_API = dict()
            for idx, (speaker, utterance) in enumerate(zip(speakers, utterances)):
                request_id = str(speaker) # if no time aggregation the id is just speaker_id
                data = json.dumps({'request_id': request_id, 'content': utterance})
                resp = self._call_API(data)
                results_API[request_id] = resp.json() # adds results to the disctionary for the key request_id
                results_API[request_id]['readability'] = readability_scores[idx]
        output_list = self._unpack_results(results_API)
        self.df_enriched_personality, \
        self.df_enriched_liwc, \
        self.df_enriched_time_orientation, \
        self.df_enriched_needs_values, \
        self.df_enriched_cognition, \
        self.df_enriched_social_dynamics, \
        self.df_enriched_drives, \
        self.df_enriched_emotions, \
        self.df_enriched_summary, \
        self.df_enriched_taxonomies = output_list

    def _prepare_df(self):
         # This function maps the conversation run time every x minutes passed into the function
        def map_run_time(minutes):
            map_run_time = []
            multiplier = 1
            for row in self.df.iterrows():
                max_minutes = multiplier * minutes * 60
                if row[1]['cum_time'] < max_minutes:
                    map_run_time.append(multiplier)
                else:
                    multiplier += 1
                    map_run_time.append(multiplier)
            return map_run_time
        min_time = pd.to_datetime(self.df['timestamp_start'].astype(str)).min()
        self.df['cum_time'] = pd.to_datetime(self.df['timestamp_end'].astype(str)).apply(lambda x: (x - min_time).total_seconds())
        map_run_time = map_run_time(self.agg_minutes)
        self.df['map_conv'] = map_run_time
        self.df['speaker_id'] = self.df['speaker_id'].astype(str)

    def _group_df(self):
        # This function groups the df and returns the lists of data to send to Receptiviti
        if self.time_aggregation: # if time aggregation
            if self.grouped: # if grouped 
                if self.speaker == 'all': # returns results for the whole group of people
                    df = self.df.groupby('map_conv')['utterance'].apply(lambda x: ' '.join(x)).reset_index()
                    df = df.sort_values('map_conv').reset_index(drop=True)
                    df['active_speaker'] = 'group'
                    speakers = df['active_speaker'].to_list()
                else: # returns results grouped by speaker and everyone else in the conversation
                    self.df['active_speaker'] = np.where(self.df['speaker_id']==self.speaker, self.speaker, 'Rest')
                    df = self.df.groupby(['active_speaker', 'map_conv'])['utterance'].apply(lambda x: ' '.join(x)).reset_index()
                    df = df.sort_values('map_conv').reset_index(drop=True)
                    speakers = df['active_speaker'].to_list()
            else: # returns results for each speaker, not grouped
                df = self.df.groupby(['speaker_id', 'map_conv'])['utterance'].apply(lambda x: ' '.join(x)).reset_index()
                df = df.sort_values('map_conv').reset_index(drop=True)
                speakers = df['speaker_id'].to_list()
        else: # if no time aggregation
            if self.grouped:
                if self.speaker == 'all':
                    speakers = ['group']
                else:
                    self.df['active_speaker'] = np.where(self.df['speaker_id']==self.speaker, self.speaker, 'Rest')
                    df = self.df.groupby('active_speaker')['utterance'].apply(lambda x: ' '.join(x)).reset_index()
                    speakers = df['active_speaker'].to_list()
            else:
                df = self.df.groupby('speaker_id')['utterance'].apply(lambda x: ' '.join(x)).reset_index()
                speakers = df['speaker_id'].to_list()
        # Below is necessary because when there is no time aggregation and the grouping is 'all' there is only one value in the list
        if (not self.time_aggregation) & (self.grouped) & (self.speaker == 'all'): 
            utterances = [' '.join(self.df['utterance'].tolist())]
            readability_scores = [textstat.flesch_reading_ease(utterances[0])]
        else:
            df['readability'] = df['utterance'].apply(textstat.flesch_reading_ease)
            utterances = df['utterance'].to_list()
            readability_scores = df['readability'].to_list()
        if self.time_aggregation: # if time aggregation returns the group time range
            conv_group = df['map_conv'].to_list()
            conv_group_range = [x*self.agg_minutes for x in conv_group]
            return speakers, utterances, conv_group_range, readability_scores
        else: # if no time aggregation does not return the group time range
            return speakers, utterances, readability_scores


    def _call_API(self, data):
        return requests.post(self.RECEPTIVITI_URL, auth=(self.RECEPTIVITI_API_KEY, self.RECEPTIVITI_API_SECRET), data=data)
        
    def _unpack_results(self, dictionary: dict) -> list:
        # This function unpack the results from Receptiviti and prepares the final df
        output_list = []
        for table, groups in self.groups.items():
            df_list = []
            for key, _ in dictionary.items():
                columns = []
                col_names = []
                for group in groups:
                    if group == 'taxonomies':
                        for metric, value in dictionary[key]['results'][0][group]['corporate_social_responsibility'].items():
                            col_names.append(metric)
                            columns.append(value)
                    else:
                        for metric, value in dictionary[key]['results'][0][group].items():
                            col_names.append(metric)
                            columns.append(value)
                    if group == 'personality':
                        col_names.append('readability')
                        columns.append(dictionary[key]['readability'])
                df_list.append(pd.DataFrame(columns, index = col_names, columns=[key]))
            df = pd.concat(df_list, axis=1)
            if self.time_aggregation:
                speakers = [x[5:] for x in df.columns]
            else:
                speakers = df.columns.tolist()
            output_df = df.T
            if self.time_aggregation:
                output_df['interval'] = [str(int(x[:4])-self.agg_minutes)+' - '+str(int(x[:4])) for x in output_df.index.tolist()]
            if not self.grouped:
                output_df['speaker_id'] = speakers
            output_df.reset_index(inplace=True, drop=True)
            if self.id_present:
                output_df['conversation_id'] = self.conversation_id
            output_list.append(output_df)
        return output_list