#ifndef WRAPPER_H
#define WRAPPER_H

template< class T >
class Wrapper{
	public:
		Wrapper()
		{
			DataPtr = 0 ;
		}
		Wrapper(const &T inner)
		{
			DataPrt = inner.clone();
		}
		~Wrapper()
		{
			if (DataPtr != 0)
				delete DataPrt;
		}

		Wrapper(const Wrapper<T>& original )
		{
			if (original.DataPtr != 0)
				DataPtr = original.DataPtr -> clone();
			else
				DataPtr = 0 ;
		}
		Wrapper& operator=(const Wrapper<T>& original)
		{
			if (this != &original)
			{	
				if(DataPtr !=0)
					delete DataPrt;
				
				DataPtr = (original.DataPtr !=0 ) ? 
					original.DataPtr->clone() : 0;
			}
			return *this;
		}
		T& operator*()
		{
			return *DataPtr;
		}

		T* operator->()
		{
			return DataPtr;
		}
	private:
		T* DataPtr;
};

#endif