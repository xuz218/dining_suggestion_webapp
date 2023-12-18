import boto3
import json
import pymysql
import os
import csv
    
def lambda_handler(event, context):
    print(event)
    
    personalize_runtime = boto3.client('personalize-runtime')
    campaign_arn = 'arn:aws:personalize:us-east-1:753967455176:campaign/campaign-latest'
    query_params = event.get('queryStringParameters', {})
    user_id = query_params.get('uid', None)
    item_ids = ['h9nuvIu8TyrQcYy8J1AOxg', 'TzhAlljC_843JO7UDDUIaQ', 'xEF3Kvd0yw74pjnlFB2Sgg', 'T8lCM6e5A4nA-epOogQzUA', 'Fit_iIDn__NPVZpVlKFBFQ', 'C2E1E0o-ssSrf_dokwxTXg', 'UjzSeETESWzramhdOdWKKQ', 'RPP_wHhM8yZYIP5W-YHk6Q', 'Q5O4qFpmPQgBN6ZaHdQcZA', 'p2zm0HnXZkI2yCAuYLb45g', '#NAME?', 'I9QmbM5vmYSA_dYM4eHeUg', '8lLs3dsSN-Am2_EtNfbXqA', 'WYdrEMBXzOcxffpQczHKww', 'WWyVq90yo4u3kWEj1Lr7rw', 'cGSLzPA_SCWrN3cyT86Nhw', '0iTaWucmr_NPSIyxUzCG1Q', 'yo_WAOnE2pPHCQduq_V_ZA', 'hD55NUiGDK7STQ8oy9QDPA', 'BQcgpQxUM39PMO_YDl_CqA', '4rWJGwb3rjDoZHA0AECa5A', 'Y2I946V78wOdwaUD9chmqg', '_WXa2M3gz2Mi0ys3s88nDw', 'yOPbrFZ2ZUsyQWsedP6gUg', '-9dqv31xBqDVAHV5iGQHsA', 'Nssb3grMQtYfJOs1HFId8A', 'MW04QetT-HjxF0tYEhiG0g', '9fydXI0fj2s-EmlF7vm8Og', 'NRQbIOVnEnsJ8t2xg7W_zg', 'XOnspIaW6mYVmrvgqOaYSQ', 'gJg_Gh2lqrCprDzR6ZP9QQ', '6nOxwnuN0ZwLX3h3JYSJnA', 'k_rLFIMOAbvchgWKEuKdtw', '8Lgz_cUAd4VFkLDpQ1xQ8w', 'K_0tNvQd7gyabfJrodf-tw', 'tbg4gR3jUUllR28cySo2kg', 'B9Mbi12NpBJkZcRtQNtMBA', 'JlxQM-azQzUECbwqDv3iTg', 'ueVSTErmXbqtN1glQd5p5A', 'Fl2z1edJw3MONc9rERWRMg', 'vHzWvZYbkoHY_071J-lPRw', 'Pfjb9Rn5Th7R-pLXVARwlA', 'bm1r5T7vc9dHws3tD6Y0sQ', '7pMyF2qq9pqMfzLZEvrohA', 'YI8UuwEIVbJ5cVQO7QKWbA', 'MD-GiizNpmFbuDIdKGzXnA', 'B87c3bE_u53yNYO1cmHSIw', 'OPSCHpuBSthP7UwnMm0GSA', 'hzhiQlyuwFt_w4-C47_Tew', 'jKDXlyPG-2rmcp9Ej6jPLA', 'JP5DnHbYWBxGRjy9_16TdQ', 'L949I6aMoUEpaY-dr-SJNw', 'dX3EgCZzY17GZC_ob5DsfA', 'm3PS0tIaa0ChcP8Y5S-DrQ', '6NcU2JAznLr9dDHp6GgQyw', 'FLKABU82NNDnCvZSZD75Bg', 'DgpnbYHVKWVuy_MC_5iiJA', '6fYGuJZXiFb282D1qJzWSQ', 'p1izzP-7YomYrP2spmOrBQ', 'V-rY0hlPjAghV14jOlVUiQ', '1uuxUq-QrUYX-Zal9TvFFQ', 'qvVltqaoMJIyO9v3Rs-E2g', 'a93NwZxjkPQydJxR42oPyg', 'S-xUsS4RKzBrOnAjy6lnyA', 'UILT56veNs63NASF3dGRKA', 'g8vu1G_fZLrPpGf2UHk6-Q', 'aYS8PnNfRHeJI-vIR6L9vA', 'yKPRuBvD3ScCc18QrZ4Y6w', 'rrxcBTWS827bJ4oBr5a_ww', '4wyPdXX96e0akxvCp268iw', '5QszELqJFqeFgpeujfknlQ', '3uJAt1EHG0x9pz_c91AHuQ', 'XO6IbZn2oxonPrfcXHK4HA', 'E0y_RtLh43VqcUrVXOuYWQ', 'YKAwpTnKO-n5vB9-pqaCLQ', 'RARUAVWONyRQovr0D6TGQg', 'herb-gOpfjJGeiYWXb2liw', '4GYc1Ld8r4rGQJKz_Qp07A', 'uCsyRxfIfiRqQQuK_JlfZA', '_BL1-CT06HGkiA3jcucu2Q', 'dvRKiQbscruyTLaAL7q3PA', 'fF-vC3L41maIXSUQDkbQ1w', 'h0Z2RZBZbiqS-Yw22WyTaQ', 'QYr9EO-2FmdpOVUjOyNjgg', '5LqclCP-RTj61-5QNo0jZw', 'iIe2lUlqiu1ibuSb37q_eg', '9BzRiWO6PSdR-l3dzCm3VA', 'ED91L2kUw_pwF_Pd1ZdViQ', 'SIpueSX4PFX1zaUsb7tmlA', '2F-7XCoPS1mbdy9ioqWuqw', 'bZZzJ2IJiL-ZAn6qen0-xA', 'Ki2-LougDEv34G5EY1sz4g', '7hh2eP4HVkyjtpcqeITk3Q', 'kwMkNIhhIexQk-nmloJlnw', '3bPnaLgZwcniU8oqi6UFDQ', 'ADEqtDQPRfZb-O3vD1bhTg', 'YRfDdBgWS4T80oJfKmVThA', '5jfJyABI5zAUk79IZXHtrw', 'deZi8F9ySV_kNyZpvYqyCg', 'n7wiN5Ergd_BSzBHVp8-SQ', '4QVG74AmkmhjE63-gwyWow', 'froxnvO6lVnzrTBS4p_W_g', 'B0qxEXABa8-t9sY4NQRRsQ', '8cycOQsmOt0ptlrBlOWdFA', 'BNZogHeuOPS3CmJNolMwJg', 'QUNchfxuTOOmjAXkHivYdQ', 'hH5PbL-5BpYKKhJhkD_kqA', 'rhWaFGReGsmyWAojvGWQlQ', 'aZzq3M2xwbNHNSQe2AbAOA', 'WuFIRXF0erQ3xfbTk6wvMA', 'h8J10FpJGaU_4OvP2MgoKQ', 'pbUj94_m12hdxy06vnsUpA', '1KGvtMU7VBcdlvxo2brdQg', 'N9cTbhwpTIcex_Je9Vx7lQ', 'DKXE-uRW-T3SvCsAEyvmqw', 'E3CvO6bRu8Kp0RzDgcvkig', 'x4_5vkcFKvaxJuZAJRX_Qw', 'l_Td-NFRIdxu7m6pgJUqhQ', 'V7_IQ1ab69JilAlgrSnMXg', 'yY1Wn_fft8T63ov0N5_rXg', 'h4co9O0SLuvhTtr_Cs9IIQ', 'jzO5HyrTtumHpe-pbUlndQ', 'wK19oQSdTF6lGKsjr9fJ-A', 'aI1yals6ghSQuXS_vMIbPw', 'HmXS5HN-E-DVMEY0mwjelg', 'NrYmqg17jU2k5Utu6DbVQQ', 'cqDVdoLA_36vpz2qxWdBqA', 'DlxYP4bABOpAGVX29Eb7Eg', 'YIYetgfNE34G8JhQu98XQw', 'rHA9M0XOJL6O11xaEiDurA']
    if user_id:
        response = personalize_runtime.get_personalized_ranking(
            campaignArn=campaign_arn,
            userId=user_id,
            inputList = item_ids
        )
        ranked_items = sorted(response['personalizedRanking'], key=lambda x: x['score'], reverse=True)
        top_10_items = ranked_items[:20]
    else:
        top_10_items = []

    return {
        'statusCode': 200,
        'body': json.dumps({'top_10_items': top_10_items})
    }
