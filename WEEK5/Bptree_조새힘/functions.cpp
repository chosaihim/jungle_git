#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

#include "bptree.h"

#define DEGREE 4
int DEGREE_t = (int)((DEGREE + 1) / 2); //=MIN_DEGREE
int MAX_DEGREE = 2 * DEGREE_t -1;

void traverse(NODE* root, int depth)
{
	printf("\n");
	NODE* node = root;
	if (node->isLeaf) {
		for (int i = 0; i < depth; i++) {
			printf("\t\t\t||");
		}
		for (int vIdx = 0; vIdx < node->N; vIdx++) {
			printf("%6d", node->key[vIdx]);
		}

		printf("\t---> : %p", node->Next);
		return;
	}
	if (!node->isLeaf) {
		for (int i = 0; i < depth; i++) {
			printf("\t\t\t||");
		}
		for (int vIdx = 0; vIdx < node->N; vIdx++) {
			printf("%6d", node->key[vIdx]);
		}
		for (int vIdx = 0; vIdx < node->N + 1; vIdx++) {
			traverse(node->child[vIdx], depth + 1);
		}
	}
}

int searchNode(NODE* root, int k)
{
	int idx = root->N-1;
	while (idx > 0 && root->key[idx] > k)
		idx--;

	if (idx >= 0 && root->key[idx] == k) {
		return true;
	}
	else if (root->isLeaf) {
		return false;
	}
	else {
		return searchNode(root->child[idx], k);
	}
}

//******CREATE*******//

NODE* createNode()
{
	NODE* newNode = (NODE*)malloc(sizeof(NODE));

	newNode->key = (int*)malloc(sizeof(int) * 4);
	newNode->child = (NODE**)malloc(sizeof(NODE*) * 4);

	newNode->N = 0;
	newNode->isLeaf = false;
	newNode->Next = NULL;

	return newNode;
}


//******INSERT*******//

void insert(NODE** root, int k) {
	NODE* tmp = *root;

	if (((*root)->N) == MAX_DEGREE) {
		NODE* new_root = createNode();
		*root = new_root;
		new_root->N = 0;
		new_root->isLeaf = false;
		new_root->Next = NULL;

		new_root->child[0] = tmp;

		splitChild(new_root, 0);
		insertNonfull(new_root, k);
	}
	else {
		insertNonfull(*root, k);
	}
}


//내가 들어갈 노드가 너무 크면 반으로 나눠두고 내려간다.
//root의 주소는 바뀌지 않고, child만 반으로 쪼개지기 때문에 NODE *root로 인자를 받을 수 있다.
void splitChild(NODE* root, int into) {

	//NODE* right = (NODE*)malloc(sizeof(NODE*));
	NODE* right = createNode();
	NODE* left = root->child[into];
	right->isLeaf = left->isLeaf;
	right->N = DEGREE_t - 1;
	left->Next = right;

	//내가 들어갈 노드가 리프이면? COPY UP
	if (left->isLeaf) {
		//일단 left와 right가 쪼개 갖는다! left는 t개, right 는 t-1개
		//key 나눠갖기
		for (int i = 0; i < DEGREE_t - 1; i++) {
			right->key[i] = left->key[DEGREE_t + i];
		}
		//child 나눠갖기
		for (int i = 0; i <= DEGREE_t - 1; i++) {
			right->child[i] = left->child[DEGREE_t + i];
		}
		right->N = DEGREE_t - 1;

		//left N개수 줄이기
		left->N = DEGREE_t;

		//parent에 값을 복사해서 올려준다.
		//parent에 자리 마련하기
		for (int i = root->N; i > into; i--) {
			root->key[i] = root->key[i - 1];
			root->child[i + 1] = root->child[i];
		}
		//값 넣기 //******어떤값을 가져오느냐가 중요
		root->key[into] = left->key[DEGREE_t - 1];
		//값이 하나 늘었으니 갯수도 하나 증가
		root->N++;
		//child 연결하기
		root->child[into + 1] = right;

	}

	//내가 들어갈 노드가 리프가 아니면? PUSH UP
	else {
		//쪼갤 index는? t-1까지만 갖고 나머지는 오른쪽을!
		//key 나눠갖기
		for (int i = 0; i < DEGREE_t - 1; i++) {
			right->key[i] = left->key[DEGREE_t + i];
		}
		//child 나눠갖기
		for (int i = 0; i <= DEGREE_t - 1; i++) {
			right->child[i] = left->child[DEGREE_t+ i];
		}
		right->N = DEGREE_t - 1;


		//left N개수 줄이기
		left->N = DEGREE_t - 1;

		//parent에 중간값 끼워넣기
		//parent에 자리 마련하기
		for (int i = root->N; i > into; i--) {
			root->key[i] = root->key[i - 1];
			root->child[i + 1] = root->child[i];
		}
		//값 넣기
		root->key[into] = left->key[DEGREE_t - 1];
		//값이 하나 늘었으니 갯수도 하나 증가
		root->N++;
		//child 연결하기
		root->child[into + 1] = right;
	}
}

//값을 넣을 준비가 된 꽉 차지 않은 노드에 값 넣기
void insertNonfull(NODE* root, int k) {
	
	//리프이면 바로 넣는다.
	//넣을 자리 찾기
	if (root->isLeaf){

		int idx = (root->N)-1;
		while (idx >= 0 && root->key[idx] > k)
			idx--;
		//뒤로 밀어주고
		for (int i = (root->N)-1; i>=idx; i--) {
			root->key[i+1] = root->key[i];
		}
		//값을 넣어준다.
		root->key[idx+1] = k;
		root->N++;
	}
	//리프가 아니면, 리프까지 내려가서 넣어야지!
	//그럼 일단 내려가야 할 곳을 찾고!
	//뚱뚱하면 split() 괜찮으면 바로 내려간다.
	else {
		int idx = (root->N) - 1;
		while (idx >= 0 && root->key[idx] > k)
			idx--;
		idx++;

		//내려가야할 곳이 뚱뚱한지 확인!
		if (root->child[idx]->N >= MAX_DEGREE) {
			splitChild(root, idx);

			//splite되서 올라온 값이 클 수도 있으니깐!
			if (k > root->key[idx]) idx++;
		}
		insertNonfull(root->child[idx], k);
	}
}


void deleteKey(NODE** root, int k)
{
	if ((*root)->isLeaf)
	{
		int idx = (*root)->N - 1;
		while (idx > 0 && (*root)->key[idx] > k)
			idx--;

		//찾았으면 idx를 덮어쓰워주는 느낌으로 delete
		for (int i = idx; i < (*root)->N; i++)
			(*root)->key[i] = (*root)->key[i + 1];
		(*root)->N--;
	}
	else
	{

		//내려갈 곳이 리프인지 아닌지를 먼저 확인해야 한다.
		int idx = (*root)->N;
		while (idx > 0 && (*root)->key[idx-1] > k)
			idx--;

		//리프임
		if ((*root)->child[idx]->isLeaf) {

			// key 가 젤 오른쪽에 존재한다.(왼쪽 형제에게 얻어오거나 합치기)
			if (idx == (*root)->N) {

				NODE* target = (*root)->child[idx];
				NODE* sibling = (*root)->child[idx-1];

				//충분! 빌리기
				if (sibling->N >= DEGREE_t) {
					//target에 자리 만들어두기
					for (int i = target->N; i > 0; i--) {
						target->key[i] = target->key[i - 1];
					}
					for (int i = target->N; i >= 0; i--) {
						target->child[i + 1] = target->child[i];
					}
					//형제 마지막값 가져오기
					target->key[0] = sibling->key[sibling->N - 1];
					//형제 마지막자식 가져오기
					target->child[0] = sibling->child[0];

					target->N = target->N++;
					sibling->N = sibling->N--;

					//root->key[idx-1]에 값 넣어주기
					(*root)->key[idx - 1] = target->key[0];
				}
				//부족! 합치기
				// 부모키 가지고 오지 않고 그대로오오오 합치기
				else {
					for (int i = 0; i < target->N; i++)
						sibling->key[DEGREE_t-1 +i] = target->key[i];
					sibling->Next = target->Next;
					(*root)->N--;
				}
			}
			// 오른쪽 형제랑 합칠 수 있는 모든 경우
			else
			{
				NODE* target = (*root)->child[idx];
				NODE* sibling = (*root)->child[idx+1];
				
				
				// >>>> 여기 짜던 중에 멈췄습니다!!! >>>>
				// 이 else문 안쪽은 수정이 필요함!!


				//충분! 빌리기
				if (sibling->N >= DEGREE_t) {
					//형제 첫번째 값 가져오기
					target->key[target->N] = sibling->key[0];
					target->child[target->N + 1] = sibling->child[0];

					//siblig 한칸씩 앞으로 당겨오기
					for (int i = sibling->N; i > 0; i--) {
						sibling->key[i] = sibling->key[i - 1];
					}
					for (int i = target->N; i >= 0; i--) {
						target->child[i + 1] = target->child[i];
					}
					//형제 마지막값 가져오기
					target->key[0] = sibling->key[sibling->N - 1];
					//형제 마지막자식 가져오기
					target->child[0] = sibling->child[0];

					target->N = target->N++;
					sibling->N = sibling->N--;

					//root->key[idx-1]에 값 넣어주기
					(*root)->key[idx - 1] = target->key[0];
				}
				//부족! 합치기
				// 부모키 가지고 오지 않고 그대로오오오 합치기
				else {
					for (int i = 0; i < target->N; i++)
						sibling->key[DEGREE_t - 1 + i] = target->key[i];
					sibling->Next = target->Next;
					(*root)->N--;
				}

			}
		}
		//리프아님
		else {
		}








	}
}