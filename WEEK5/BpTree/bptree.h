#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>



typedef struct _NODE {
	struct _NODE** C;
	struct _NODE* Next;
	int* Key;
	int N;
	bool isLeaf;
}Node;

int searchNode(Node* root, int k);
// 노드 초기화, 노드 탐색, 값 삽입 - (트리 기준, non-full), 자녀 분리
Node* createNode();
void insertTree(Node** root, int k);
void insertNonfull(Node* root, int k);
void splitChild(Node* parent, int idx);
void deleteTree(Node** root, int k);
void printAll(Node* root, int depth);