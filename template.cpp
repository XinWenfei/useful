#include<iostream>
using namespace std;

template <typename T>
class Functor{
    public:
        virtual int operator()(T arg) = 0;
};

template <typename T, typename ARG>
class SpecificFunctor : public Functor<ARG>{
    public:
        SpecificFunctor(T* p, int (T::*_pmi)(ARG arg)){
            m_p = p;
            m_pmi = _pmi;
        }

        virtual int operator()(ARG arg){
            (*m_p.*m_pmi)(arg);
        }

    private:
        int (T::*m_pmi)(ARG arg);
        T* m_p;
};

class A{
    public:
        A (int a0):a(a0){}
        int Hello(int b0)
        {
            cout<<"hello from A, a = "<<a<<", b0="<<b0<<endl;
        }
        int a;
};

int main()
{
    A a(10);
    SpecificFunctor<A, int> sf(&a, &A::Hello);
    sf(5);
}
