import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./config/key.json")
firebase_admin.initialize_app(cred)


class FirePost:
    @staticmethod
    def send_global_data_to_firebase(**args):
        to_send_dict = {
            "totalInfected": args['total_infected'],
            "totalDead": args['total_dead'],
            "totalRecovered": args['total_recovered'],
        }

        db = firestore.client()
        db.collection('corona').document('global').set(to_send_dict)

    @staticmethod
    def send_local_data_to_firebase(**args):
        to_send_dict = {
            "country": args['country'],
            "totalCases": args['total_cases'],
            "newCases": args['new_cases'],
            "totalDeaths": args['total_deaths'],
            "newDeaths": args['new_deaths'],
            "totalRecovered": args['total_recovered'],
            "activeCases": args['active_cases'],
            "seriousCritical": args['critical'],
            "totalCasesPerMillion": args['total_case_per_million'],
        }

        db = firestore.client()
        db.collection('corona').document('local').set(to_send_dict)
