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
// ��� �ʱ�ȭ, ��� Ž��, �� ���� - (Ʈ�� ����, non-full), �ڳ� �и�
Node* createNode();
void insertTree(Node** root, int k);
void insertNonfull(Node* root, int k);
void splitChild(Node* parent, int idx);
void deleteTree(Node** root, int k);
void printAll(Node* root, int depth);