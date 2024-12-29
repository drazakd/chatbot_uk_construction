# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re

class ActionCalculCout(Action):
    def name(self) -> Text:
        return "action_calcul_cout"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        superficie = tracker.get_slot("superficie")
        try:
            if superficie:
                superficie = float(superficie)
                cout = superficie * 1000  # Exemple de calcul : £1000/m²
                dispatcher.utter_message(text=f"Le coût estimé pour {superficie}m² est de £{cout:.2f}.")
            else:
                dispatcher.utter_message(text="Pouvez-vous préciser la superficie pour estimer le coût ?")
        except ValueError:
            dispatcher.utter_message(text="Désolé, je n'ai pas compris la superficie. Veuillez indiquer un chiffre.")
        return []

class ActionCalculTemps(Action):
    def name(self) -> Text:
        return "action_calcul_temps"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        superficie = tracker.get_slot("superficie")
        try:
            if superficie:
                superficie = float(superficie)
                temps = superficie / 20  # Exemple : 20m² construits par mois
                dispatcher.utter_message(text=f"La durée estimée pour {superficie}m² est de {temps:.1f} mois.")
            else:
                dispatcher.utter_message(text="Pouvez-vous préciser la superficie pour estimer la durée ?")
        except ValueError:
            dispatcher.utter_message(text="Désolé, je n'ai pas compris la superficie. Veuillez indiquer un chiffre.")
        return []

class ActionDemanderDetailsProjet(Action):
    def name(self) -> Text:
        return "action_demander_details_projet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Pouvez-vous fournir des détails sur votre projet ? Par exemple, la superficie, le type de bâtiment, et le lieu.")
        return []

class ActionCalculSuperficie(Action):

    def name(self) -> str:
        return "action_calcul_superficie"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Récupérer la superficie à partir du slot
        superficie = tracker.get_slot("superficie")
        
        # Vérification si la superficie a été extraite correctement
        if superficie:
            try:
                # Extraire un nombre de la superficie (ex: 150m²)
                superficie_value = re.findall(r"\d+", superficie)
                
                if superficie_value:
                    superficie_value = int(superficie_value[0])  # convertir en entier
                    # Exemple de calcul (ici, un prix par m² pour une estimation basique)
                    estimation = superficie_value * 1000  # par exemple 1000 par m²
                    dispatcher.utter_message(text=f"Le prix estimé pour une superficie de {superficie_value} m² est de {estimation} €.")
                else:
                    dispatcher.utter_message(text="Je n'ai pas pu extraire la superficie, pouvez-vous répéter ?")
            
            except Exception as e:
                dispatcher.utter_message(text=f"Une erreur est survenue lors du calcul : {str(e)}")
        else:
            dispatcher.utter_message(text="Je n'ai pas reçu de superficie, pouvez-vous me la fournir ?")
        
        return [SlotSet("superficie", None)]  # Réinitialiser le slot après l'action