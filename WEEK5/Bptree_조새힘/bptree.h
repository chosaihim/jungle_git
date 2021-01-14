#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

typedef struct _NODE {
	
	struct _NODE** child;
	int *key;
	int N;
	bool isLeaf; 
	
	struct _NODE* Next;
}NODE;




void traverse(NODE* root, int depth);
int searchNode(NODE* root, int k);

NODE* createNode();

void insert(NODE** root, int k);
void splitChild(NODE* root, int into);
void insertNonfull(NODE* root, int k);

void deleteKey(NODE** root, int k);