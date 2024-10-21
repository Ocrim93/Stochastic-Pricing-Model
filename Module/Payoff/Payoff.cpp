#include "Payoff.h"
#include <algorithm>

PayOffCall::PayOffCall(double Strike_) : Strike(Strike_){

}

double PayOffCall::operator() (double Spot) const{
	return std::max(Spot - Strike,0.0);
}

PayOffPut::PayOffPut(double Strike_) : Strike(Strike_){

}

double PayOffPut::operator() (double Spot) const{
	return std::max(Strike - Spot,0.0);
}

PayOffDoubleDigital::PayOffDoubleDigital(double LowerLevel_, double UpperLevel_)
	:LowerLevel(LowerLevel_),UpperLevel(UpperLevel_){

	}

// DoubleDigital payOff . It pays 1 if spot is between two values and 0 otherwise
double PayOffDoubleDigital::operator()(double Spot) const{
	if (Spot <= LowerLevel){
		return 0;
	}
	if (Spot >= UpperLevel){
		return 0;
	}
	return 1;
}