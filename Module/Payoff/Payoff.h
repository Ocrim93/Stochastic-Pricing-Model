#ifndef PAYOFF_H
#define PAYOFF_H

#include <map>
#include <string>

class PayOff{

	public:
		PayOff(){}
		//Deleting a derived class object using a pointer of base class type 
		//that has a non-virtual destructor results in undefined behaviour.
		//Making base class destructor virtual guarantees that the object of derived class is destructed properly.
		virtual ~PayOff(){}
		virtual PayOff* clone() const=0;
		virtual double Value(double Expiry_, double Spot_, double Vol_, double r_) const = 0 ;
		
		std::map<std::string,double> Greeks() const;
		double Value_perVol(double Vol_) const;
		double Vega_perVol(double Vol_) const;
		double ImpliedVolNewtonRaphson(double MtM, double starting, double accuracy) const;
		double ImpliedVolBisection(double MtM, double Low, double High, double  accuracy ) const;

	//overloading operator()
		// const method 
	// being a virtual function, the operator() has a =0 after it. 
	// This means that that it is a pure virtual function. A pure virtual function has the property that it does  
	// not need to be defined in the base class and must be defined in an inherited class 
		virtual double operator()(double Spot_) const = 0;
		double Expiry;
		double Spot;
		double Vol;
		double r;

	private:
};

#endif

