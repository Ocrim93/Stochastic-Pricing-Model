#ifndef VANILLA_H
#define VANILLA_H

#include "../Payoff.h"

class VanillaCall : public PayOff{
	public:
		VanillaCall(double Strike_, double Expiry_);
		virtual ~VanillaCall(){}
		virtual PayOff* clone() const;
		virtual double operator()(double Spot) const;
		double GetExpiry() const;
	private:
		double Strike;
		double Expiry;

};

class VanillaPut : public PayOff{
	public:
		VanillaPut(double Strike_,double Expiry_);
		virtual ~VanillaPut(){}
		virtual PayOff* clone() const;
		virtual double operator()(double Spot) const;
		double GetExpiry() const;
	private:
		double Strike;
		double Expiry;
};

#endif 