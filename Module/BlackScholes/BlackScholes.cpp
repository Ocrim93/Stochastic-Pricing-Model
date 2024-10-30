#include "BlackScholes.h"
#include "../Random/Random.h"
#include "../Payoff/Payoff.h"
#include <cmath>


double BlackScholesPathIndependent( const PayOff& thePayOff,
									double Spot,
									double Vol,
									double r,
									double q,
									unsigned long NumberOfPaths){

	double Expiry = thePayOff.GetExpiry();
	double fixedPart = (r - Vol*Vol/2 - q )*Expiry;
	double sumPayOff = 0 ;

	for (unsigned long i = 0 ; i < NumberOfPaths; i++){
		double final_S = Spot*exp(fixedPart +  Vol*sqrt(Expiry)*GetOneGaussianByBoxMuller());
		sumPayOff += thePayOff(final_S);
	 
	}
	double expectedPayOff = sumPayOff/NumberOfPaths;
	expectedPayOff *= exp(-r*Expiry);

	return expectedPayOff;
}