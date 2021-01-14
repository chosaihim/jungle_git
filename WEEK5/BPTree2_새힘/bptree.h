#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

typedef struct _NODE {
	
	struct _NODE** child;
	int *key;
	int *data;
	int N;
	bool isLeaf; 
	
	struct _NODE* Next;
}NODE;




void traverse(NODE* root, int depth);
int searchNode(NODE* root, int k);

NODE* createNode();

void insert(NODE** root, int k, int data);
void splitChild(NODE* root, int into);
void insertNonfull(NODE* root, int k, int data);

void deleteKey(NODE** root, int k);

// 확인 함수
void print_for_exam(NODE* cur);