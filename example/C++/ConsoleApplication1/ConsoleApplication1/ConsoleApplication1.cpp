// ConsoleApplication1.cpp : 此檔案包含 'main' 函式。程式會於該處開始執行及結束執行。
//
//#define MULTIPLEBBOXONE
#include "stdio.h"
#include "pch.h"
#include <iostream>
#include <string>
#include <array>
#include <msclr/marshal.h>        // .NET string to C-style string
#include <msclr/marshal_cppstd.h> // .NET string to STL string
using namespace System;
using namespace BBoxAPI;
using namespace msclr::interop;


int main()
{
	BBoxAPI::BBoxOneAPI ^b = gcnew BBoxAPI::BBoxOneAPI();

	//array<String ^>^ strarray = b->getStringArray();

	//array<String^>^ strarray = gcnew array<String^>(2);
	//for (int i = 0; i < 2; i++)
	//	strarray[i] = String::Concat("Number ", i.ToString());

	//for (int i = 0; i < strarray->Length; i++)
	//	Console::WriteLine("aa" + strarray[i]);

	//String^ net_s = "Hello .NET";
	//std::string nodename[2] = {"001", "110"}; // uses STL string, not .NET String
	//std::cout<< nodename[0]+"\n";
	//
	//marshal_context^ context = gcnew marshal_context();
	//const char* c_s = context->marshal_as<const char*>(net_s);
	//std::cout << c_s;
	////printf("%s\n", c_s);

	array<String ^>^ dev_info = b->ScanningDevice();

	// suppose only one bboxone device
	array<String^>^ info_arr = dev_info[0]->Split(',');

	for (int i = 0; i < info_arr->Length; i++)
		Console::WriteLine(info_arr[i]);

	
	

	/* It will send the init command to BBoxOne. */
	String^ sn = info_arr[0]; // sn
	String^ s_info = b->Init(sn, 0/*BBoxOne*/, 0);

	Console::WriteLine(s_info);

	b->selectAAKit("TMYTEK_4x4", sn);
	
	b->SwitchTxRxMode(0/*Tx*/, sn);

	b->getTxRxMode(sn);




	Console::WriteLine("press enter to continue....");
	Console::Read();

	int deg = 10;
	
	for (int count = 0; count < 1; count++)
	{
		try
		{
			s_info = b->setBeamX(0/*dB*/, deg/*degree*/, sn);
			Console::WriteLine(s_info);
			s_info = b->setBeamY(0/*dB*/, deg/*degree*/, sn);
			Console::WriteLine(s_info);
			s_info = b->setBeamXY(0/*dB*/, deg/*degree*/, deg/*degree*/, sn);
			Console::WriteLine(s_info);
		}
		catch (...)
		{
			Console::WriteLine("An error occurred.");
		}
	}


	Console::Read();



}

// 執行程式: Ctrl + F5 或 [偵錯] > [啟動但不偵錯] 功能表
// 偵錯程式: F5 或 [偵錯] > [啟動偵錯] 功能表

// 開始使用的秘訣: 
//   1. 使用 [方案總管] 視窗，新增/管理檔案
//   2. 使用 [Team Explorer] 視窗，連線到原始檔控制
//   3. 使用 [輸出] 視窗，參閱組建輸出與其他訊息
//   4. 使用 [錯誤清單] 視窗，檢視錯誤
//   5. 前往 [專案] > [新增項目]，建立新的程式碼檔案，或是前往 [專案] > [新增現有項目]，將現有程式碼檔案新增至專案
//   6. 之後要再次開啟此專案時，請前往 [檔案] > [開啟] > [專案]，然後選取 .sln 檔案
