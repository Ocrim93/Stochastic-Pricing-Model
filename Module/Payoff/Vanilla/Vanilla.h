#ifndef VANILLA_H
#define VANILLA_H

#include "../Payoff.h"
#include "../../Taxonomy.h"

class VanillaCall : private PayOff{
	public:
		VanillaCall(double Strike_, double Expiry_, double Spot_ ,double Vol,double r_, double q_ );
		virtual ~VanillaCall(){}
		virtual PayOff* clone() const;
		virtual double operator()(double Spot) const;
		double Value() const ;
		double ImpliedVolBisection(double MtM, double Low, double High) const;
		double Value_perVol(double Vol_) const;
		void SetNumberOfPaths(unsigned long NumberOfPaths_) ;
		void SetAccuracy(double accuracy_);


		unsigned long NumberOfPaths;
		double accuracy;

	 	double Expiry;
		double Spot;
		double Vol;
		double r;
		double q;
	private:
		double Strike;
		

};


#endif 