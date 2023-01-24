#include <iostream>
#include <vector>
#include <string>

using namespace std;


//Adding numbers
int summation(int num1, int num2)
{
    return num1+num2;
}

//Multiplying
int multiplying(int num1, int num2)
{
    return num1*num2;
}


//Testing outputs
int main()
{
    vector<int> msg {10,5,16,20,30,25,1};
    int x {31};
    int y {10};
    int sum {0};

    cout<< "Adding Numbers!"<<endl;

    for (const int& word : msg)
    {
        cout << sum << "+" << word <<"=";
        sum = summation(sum,word);
        cout << sum << endl;
    }
    
    cout<< endl << "Multiplying Numbers!"<<endl;

    for (const int& word : msg)
    {
        cout << sum << "*" << word <<"=";
        sum = multiplying(sum,word);
        cout << sum << endl;
    }

    cout << "Done!" << endl;
}


