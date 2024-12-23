#ifndef DOUBLEDIGITAL_H
#define DOUBLEDIGITAL_H
#include "../Payoff.h"

class DoubleDigital : public PayOff
{
	public:
		DoubleDigital(double LowerLevel_, double UpperLevel_, double Expiry_);
		virtual ~DoubleDigital(){};
		virtual double operator() (double Spot) const;
		virtual PayOff* clone() const;
		double GetExpiry() const;
		double Value(double Spot,double Vol, double r, double q, unsigned long NumberOfPaths) const ;

	private:
		double Expiry;
		double LowerLevel;
		double UpperLevel;
}
#endif 