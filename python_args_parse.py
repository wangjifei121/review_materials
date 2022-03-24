#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @file: parse_test.py
# Date: 2022/3/24

import argparse

import argparse

parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('--parent', type=int)

parser = argparse.ArgumentParser(
    prog='my_test',  # 名称 - 默认为脚本名
    description='args parse learn',  # 命令前置描述
    epilog='this is a end description',  # 后置描述
    parents=[parent_parser],  # 父解析器 add_help=False
    add_help=True,  # 帮助信息

)
parser.add_argument('IP', help='位置参数描述', type=str)
parser.add_argument('-p', help='可选参数描述', required=True, type=int)
parser.add_argument('-n', help='默认值为const参数', action='store_const', const=5555)  # 提供默认值
parser.add_argument('-t', help='默认值为true参数', action='store_true')  # 提供默认值true
parser.add_argument('-f', help='默认值为false参数', action='store_false')  # 提供默认值false
parser.add_argument('-a', help='可重复使用的参数', action='append')  # 提供可重复使用的参数
parser.add_argument('-ns', help='多值的参数', nargs=2, type=int)  # 提供多值参数
parser.add_argument('-d', help='默认值的参数', default='file', type=str)  # 提供默认值参数
parser.add_argument('-m', help='默认选项的参数', choices=['keyword', 'model'], type=str)  # 提供默认选项的参数
parser.add_argument('-s', '--sort', help='参数转化', default='created')  # 参数转化 s -> sort

args = parser.parse_args()

print(args)
