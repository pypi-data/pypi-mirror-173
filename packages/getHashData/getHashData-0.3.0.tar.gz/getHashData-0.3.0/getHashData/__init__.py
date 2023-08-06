# -*- coding: utf-8 -*-
import binascii
import time

from eth_account.messages import encode_defunct
from web3 import Web3, HTTPProvider
import argparse
import os
import re


def dealData(data, isFunction):
    params = []
    try:
        if data.find(' ') == -1:
            dataList = re.findall(r'([a-zA-Z0-9_]*)\((.*?)\)', data)
        else:
            if isFunction:
                dataList = re.findall(r'function\s([a-zA-Z0-9_]*)\s{0,10}\((.*?)\)', data)
            else:
                dataList = re.findall(r'event\s([a-zA-Z0-9_]*)\s{0,10}\((.*?)\)', data)
            if len(dataList) == 0:
                dataList = re.findall(r'([a-zA-Z0-9_]*)\s{0,10}\((.*?)\)', data)

        name = dataList[0][0]
        paramsWithVariable = dataList[0][1].split(',')
        if len(paramsWithVariable) == 0:
            paramsWithVariable = dataList[0][1]
        for param in paramsWithVariable:
            temp = param.strip().split(' ')
            if len(temp) > 0:
                temp = temp[0]
            else:
                temp = param.strip()
            if temp == "uint":
                temp = "uint256"
            params.append(temp)
        finalParam = ','.join(params)
        returnData = f'{name}({finalParam})'
        return returnData
    except Exception as e:
        print("--------------------------------------")
        print("error line:", e.__traceback__.tb_lineno)
        print("error type:", e)
        print("--------------------------------------")
        os._exit(0)


def getData(path, isFunction):
    try:
        with open(path, 'r+', encoding='utf8') as fs:
            data = ''.join(fs.readlines()).replace('\n', '')
        if isFunction:
            eventsOrfunctions = re.findall(r'function\s[a-zA-Z0-9_]*\s{0,10}\(.*?\)', data)
        else:
            eventsOrfunctions = re.findall(r'event\s[a-zA-Z0-9_]*\s{0,10}\(.*?\)', data)
        return eventsOrfunctions
    except Exception as e:
        print("--------------------------------------")
        print("error line:", e.__traceback__.tb_lineno)
        print("error type:", e)
        print("--------------------------------------")
        os._exit(0)


def _argparse():
    parser = argparse.ArgumentParser(description="To get functions or events hash.")
    parser.add_argument('-s', default='', dest='String', help='Choose a string as input.')
    parser.add_argument('-i', default='', dest='inputFile', help='Input file path and name.')
    parser.add_argument('-o', default='', dest='outputFile', help='Output file path and name. Default is None.')
    parser.add_argument('-w', action="store_true", dest='web3', help='Use web3.')
    parser.add_argument('-f', action="store_true", dest='type', help='Use funtion.')
    parser.add_argument('-k', default='', dest='PrivateKey', help='Provide a key to sign message.')
    parser.add_argument('-d', default='', dest='Data', help='Message to sign.')
    parser.add_argument('--hex', default='', dest='HexData', help='Hex message to sign.')
    parser.add_argument('--sign', action="store_true", dest='Sign', help='Sign a message.')
    return parser.parse_args()


def main():
    hashList = []
    try:
        parser = _argparse()
        isFile = parser.inputFile != ''
        outputPath = parser.outputFile
        isUseWeb3 = parser.web3
        isFunction = parser.type
        isSign = parser.Sign
        privateKey = parser.PrivateKey
        data = parser.Data
        hexData = parser.HexData
        wb3 = None
        sha3 = None
        if isUseWeb3 or isSign:
            module = __import__('web3')
            wb3 = module.Web3()
        else:
            sha3 = __import__('sha3')
        if isFile:
            inputPath = parser.inputFile
            eventsOrfunctions = getData(inputPath, isFunction)
            for item in eventsOrfunctions:
                item = dealData(item, isFunction)
                if isUseWeb3:
                    hashData = wb3.sha3(text=item).hex()
                else:
                    k = sha3.keccak_256()
                    k.update(item.encode('utf-8'))
                    hashData = '0x' + k.hexdigest()
                if isFunction:
                    hashData = hashData[:10]
                if hashData in hashList:
                    continue
                hashList.append(hashData)
                print(hashData, item)
                if outputPath != '':
                    with open(outputPath, 'a+', encoding='utf-8') as fa:
                        fa.write(f'{hashData}\t{item}\n')
        elif isSign:
            module = __import__('web3')
            wb3 = module.Web3()
            if privateKey != "" and (data != "" or hexData != ""):
                if hexData != "":
                    signed_msg = wb3.eth.account.signHash(hexData, privateKey)
                elif data != "":
                    signed_msg = wb3.eth.account.sign_message(encode_defunct(text=data), privateKey)
                print(
                    f"messageHash: {list(signed_msg)[0].hex()}\nr: {list(signed_msg)[1]}\ns: {list(signed_msg)[3]}\nv: {list(signed_msg)[2]}")
                print(f"signature: {list(signed_msg)[4].hex()}")
            else:
                print("Lack of privateKey or data.")
        else:
            item = parser.String
            if item == "":
                print('please choose file or string as input.')
                os._exit(0)
            item = dealData(item, isFunction)
            if isUseWeb3:
                hashData = wb3.sha3(text=item).hex()
            else:
                k = sha3.keccak_256()
                k.update(item.encode('utf-8'))
                hashData = '0x' + k.hexdigest()
            if isFunction:
                hashData = hashData[:10]
            print(hashData, item)
            if outputPath != '':
                with open(outputPath, 'a+', encoding='utf-8')as fa:
                    fa.write(f'{hashData}\t{item}\n')
    except Exception as e:
        print("--------------------------------------")
        print("error line:", e.__traceback__.tb_lineno)
        print("error type:", e)
        print("--------------------------------------")
        os._exit(0)


if __name__ == '__main__':
    main()
