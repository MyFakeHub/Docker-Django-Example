import argparse
import sys
import pandas as pd
import numpy as np
import pickle
from random import randint
import math


sim = None
reco = None
vas_users = None
non_vas_users = None
vas_data = None

vas_msisdns = None
non_vas_msisdns = None


def inspect_vas_user(msisdn):
    global sim
    global reco
    global vas_users
    global non_vas_users
    global vas_data
    global vas_msisdns
    global non_vas_msisdns

    vas_profile = vas_users[vas_users['MSISDN'] == msisdn]
    taken_vas = vas_data[vas_data['MSISDN'] == msisdn]

    return vas_profile, taken_vas

def inspect_non_vas_user(msisdn):
    global sim
    global reco
    global vas_users
    global non_vas_users
    global vas_data
    global vas_msisdns
    global non_vas_msisdns

    with open('tensorflow/non_vas_users_index.pkl', 'rb') as f:
        non_vas_index = pickle.load(f)

    non_vas_user_id = non_vas_index[msisdn]

    similarities = sim[sim['Non-VAS_User'] == non_vas_user_id]
    similarities['VAS_User'] = vas_msisdns[similarities['VAS_User']]
    similarities = similarities.rename(columns={'VAS_User': 'MSISDN'})

    vas_user_ids = sim[sim['Non-VAS_User'] == non_vas_user_id]['VAS_User'].values
    vas_msisdn = vas_msisdns[vas_user_ids]
    non_vas_msisdn = non_vas_msisdns[non_vas_user_id]

    vas_profile = vas_users[vas_users['MSISDN'].isin(vas_msisdn)].merge(similarities, on=['MSISDN']).drop(columns=['Non-VAS_User'])
    non_vas_profile = non_vas_users[non_vas_users['MSISDN'] == non_vas_msisdn]

    taken_vas = vas_data[vas_data['MSISDN'].isin(vas_msisdn)]
    recommendations = reco[reco['Non-VAS_User'] == non_vas_msisdn]
    
    assert int(msisdn) == non_vas_msisdn
    return vas_profile, non_vas_profile, taken_vas, recommendations
    
def inspect_user(kwargs):
    msisdn = kwargs.msisdn
    global sim
    global reco
    global vas_users
    global non_vas_users
    global vas_data
    global vas_msisdns
    global non_vas_msisdns
    
    sim = pd.read_csv('tensorflow/euclidean_similarities_full_k=3.csv')
    reco = pd.read_csv('tensorflow/TEST_euclidean_similarities_recommendations_full_final_final.csv')
    vas_users = pd.read_csv('tensorflow/vas_users.csv')
    non_vas_users = pd.read_csv('tensorflow/non_vas_users.csv')
    vas_data = pd.read_csv('tensorflow/vas_data.csv')
    
    vas_msisdns = vas_users.MSISDN.values
    non_vas_msisdns = non_vas_users.MSISDN.values

    if int(msisdn) in non_vas_msisdns:
        vas, non_vas, taken_vas, recommendations = inspect_non_vas_user(int(msisdn))
        vas = vas.set_index('MSISDN').round({'CONSUMPTION': 2,
                                            'REFILL_AMOUNT': 2,
                                            'INCOMING_CALL_MINUTES': 2,
                                            'OUTGOING_CALL_MINUTES': 2,
                                            'INCOMING_CALL_COUNT': 2,
                                            'OUTGOING_CALL_COUNT': 2,
                                            'DATA_VOLUME': 2,
                                            'Similarity': 7
                                            }).to_dict(orient='index')
        non_vas = non_vas.set_index('MSISDN').round({'CONSUMPTION': 2,
                                                    'REFILL_AMOUNT': 2,
                                                    'INCOMING_CALL_MINUTES': 2,
                                                    'OUTGOING_CALL_MINUTES': 2,
                                                    'INCOMING_CALL_COUNT': 2,
                                                    'OUTGOING_CALL_COUNT': 2,
                                                    'DATA_VOLUME': 2,
                                                    'Similarity': 7
                                                    }).to_dict(orient='index')
        with open('tensorflow/result_type.pkl', 'wb') as f:
            pickle.dump('Non-VAS', f)
        with open('tensorflow/result_vas.pkl', 'wb') as f:
            pickle.dump(vas, f)
        with open('tensorflow/result_non_vas.pkl', 'wb') as f:
            pickle.dump(non_vas, f)
        with open('tensorflow/result_taken_vas.pkl', 'wb') as f:
            pickle.dump(taken_vas.groupby(['MSISDN', 'SERVICE_NAME']).sum().reset_index().drop(columns=['SUBSCRIBER_ID']).to_dict(orient='index'), f)
        with open('tensorflow/result_recommendations.pkl', 'wb') as f:
            pickle.dump(recommendations.rename(columns={'Non-VAS_User': 'MSISDN'}).to_dict(orient='index'), f)
    else:
        vas, taken_vas = inspect_vas_user(int(msisdn))
        vas = vas.set_index('MSISDN').round({'CONSUMPTION': 2,
                                            'REFILL_AMOUNT': 2,
                                            'INCOMING_CALL_MINUTES': 2,
                                            'OUTGOING_CALL_MINUTES': 2,
                                            'INCOMING_CALL_COUNT': 2,
                                            'OUTGOING_CALL_COUNT': 2,
                                            'DATA_VOLUME': 2,
                                            'Similarity': 7
                                            }).to_dict(orient='index')
        with open('tensorflow/result_type.pkl', 'wb') as f:
            pickle.dump('VAS', f)
        with open('tensorflow/result_vas.pkl', 'wb') as f:
            pickle.dump(vas, f)
        with open('tensorflow/result_taken_vas.pkl', 'wb') as f:
            pickle.dump(taken_vas.groupby(['MSISDN', 'SERVICE_NAME']).sum().reset_index().drop(columns=['SUBSCRIBER_ID']).to_dict(orient='index'), f)

def inspect():
    global sim
    global reco
    global vas_users
    global non_vas_users
    global vas_data
    global vas_msisdns
    global non_vas_msisdns

    non_vas_user_id = randint(0, 3193023)
    similarities = sim[sim['Non-VAS_User'] == non_vas_user_id]
    similarities['VAS_User'] = vas_msisdns[similarities['VAS_User']]
    similarities = similarities.rename(columns={'VAS_User': 'MSISDN'})

    vas_user_ids = sim[sim['Non-VAS_User'] == non_vas_user_id]['VAS_User'].values
    vas_msisdn = vas_msisdns[vas_user_ids]
    non_vas_msisdn = non_vas_msisdns[non_vas_user_id]

    vas_profile = vas_users[vas_users['MSISDN'].isin(vas_msisdn)].merge(similarities, on=['MSISDN']).drop(columns=['Non-VAS_User'])
    non_vas_profile = non_vas_users[non_vas_users['MSISDN'] == non_vas_msisdn]

    taken_vas = vas_data[vas_data['MSISDN'].isin(vas_msisdn)]
    recommendations = reco[reco['Non-VAS_User'] == non_vas_msisdn]
            
    return vas_profile, non_vas_profile, taken_vas, recommendations

def inspect_random_user(kwargs):
    global sim
    global reco
    global vas_users
    global non_vas_users
    global vas_data
    global vas_msisdns
    global non_vas_msisdns
    
    sim = pd.read_csv('tensorflow/euclidean_similarities_full_k=3.csv')
    reco = pd.read_csv('tensorflow/TEST_euclidean_similarities_recommendations_full_final_final.csv')
    vas_users = pd.read_csv('tensorflow/vas_users.csv')
    non_vas_users = pd.read_csv('tensorflow/non_vas_users.csv')
    vas_data = pd.read_csv('tensorflow/vas_data.csv')
    
    vas_msisdns = vas_users.MSISDN.values
    non_vas_msisdns = non_vas_users.MSISDN.values

    vas, non_vas, taken_vas, recommendations = inspect()
    vas = vas.set_index('MSISDN').round({'CONSUMPTION': 2,
                                        'REFILL_AMOUNT': 2,
                                        'INCOMING_CALL_MINUTES': 2,
                                        'OUTGOING_CALL_MINUTES': 2,
                                        'INCOMING_CALL_COUNT': 2,
                                        'OUTGOING_CALL_COUNT': 2,
                                        'DATA_VOLUME': 2,
                                        'Similarity': 7
                                        }).to_dict(orient='index')
    non_vas = non_vas.set_index('MSISDN').round({'CONSUMPTION': 2,
                                                'REFILL_AMOUNT': 2,
                                                'INCOMING_CALL_MINUTES': 2,
                                                'OUTGOING_CALL_MINUTES': 2,
                                                'INCOMING_CALL_COUNT': 2,
                                                'OUTGOING_CALL_COUNT': 2,
                                                'DATA_VOLUME': 2,
                                                'Similarity': 7
                                                }).to_dict(orient='index')

    with open('tensorflow/result_vas.pkl', 'wb') as f:
        pickle.dump(vas, f)
    with open('tensorflow/result_non_vas.pkl', 'wb') as f:
        pickle.dump(non_vas, f)
    with open('tensorflow/result_taken_vas.pkl', 'wb') as f:
        pickle.dump(taken_vas.groupby(['MSISDN', 'SERVICE_NAME']).sum().reset_index().drop(columns=['SUBSCRIBER_ID']).to_dict(orient='index'), f)
    with open('tensorflow/result_recommendations.pkl', 'wb') as f:
        pickle.dump(recommendations.rename(columns={'Non-VAS_User': 'MSISDN'}).to_dict(orient='index'), f)


def check_arg(args=None):
    parser = argparse.ArgumentParser(
            description='DB pipeline')
    parser.add_argument('-a', '--action',
                        help='action to take',
                        required='True')
    parser.add_argument('-m', '--msisdn',
                        help='MSISDN of user to inspect',
                        required=False)
    _results = parser.parse_args(args)
    return _results


if __name__ == '__main__':
    results = check_arg(sys.argv[1:])
    globals()[results.action](results)
