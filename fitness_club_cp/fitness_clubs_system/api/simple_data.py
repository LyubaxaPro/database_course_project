from manager.repositories import FitnessClubsRepository, InstructorsRepository, CustomUserRepository, SpecialOffersRepository, PricesRepository

from .role import *
from .instructor_schedule import *
def prices_f(request):
    special_offers = SpecialOffersRepository.read_all(request.user)
    prices = PricesRepository.read_all(request.user)
    return {'special_offers': special_offers, 'prices': prices}

