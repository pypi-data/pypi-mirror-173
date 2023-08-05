"""Implement Token Service"""

from getnet.services.service import Service as BaseService
from getnet.services.verification.card_verification import CardVerification
from getnet.services.verification.card_verified import CardVerified


class Service(BaseService):
    """Represents the token service operations"""

    path = "/v1/cards/verification"

    def verification(self, card: CardVerification):
        """Generate an token for the card data

        Args:
            card (Card:
        """


        self._client.request.headers = (
            {
                "Accept":"application/json, text/plain, */*",
                "Authorization": "Bearer {}".format(self._client.access_token),
                "Content-Type":"application/json"
            }
        )
        
        response = self._post(self.path, json=card.as_dict())
        return CardVerified(response.get("status"))
