#ifndef PAYOFF_H
#define PAYOFF_H

class PayOff{

	public:
		PayOff(){}
		//Deleting a derived class object using a pointer of base class type 
		//that has a non-virtual destructor results in undefined behaviour.
		//Making base class destructor virtual guarantees that the object of derived class is destructed properly.
		virtual ~PayOff(){}

	//overloading operator()
		// const method 
	// being a virtual function, the operator() has a =0 after it. 
	// This means that that it is a pure virtual function. A pure virtual function has the property that it does not 
	// need to be defined in the base class and must be defined in an inherited class 
	virtual double operator()(double Spot) const = 0;
	
	private:
};

class PayOffCall : public PayOff{
	public:
		PayOffCall(double Strike_);
		virtual ~PayOffCall(){};
		virtual double operator(double Spot) const;
	private:
		double Strike;

};

class PayOffPut : public PayOff{
	public:
		PayOffPut(double Strike_);
		virtual ~PayOffPut(){};
		virtual double operator(double Spot) const;
	private:
		double Strike;

};

class PayOffDoubleDigital : public PayOff{
	public:
		PayOffDoubleDigital(double LowerLevel_, double UpperLevel_);
		virtual ~PayOffDoubleDigital(){};
		virtual double operator()(double Spot) const;
	private:
		double LowerLevel;
		double UpperLevel;

};

#endif

