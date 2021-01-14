#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

#include "bptree.h"

#define DEGREE 4
int DEGREE_t = (int)((DEGREE + 1) / 2); //=MIN_DEGREE
int MAX_DEGREE = DEGREE -1;


// 출력(DFS)
void print_for_exam(NODE* cur) {
	if (cur->isLeaf) {
		for (int i = 0; i < cur->N; i++) {
			printf("[%5d, %5d]\n", cur->key[i], cur->data[i]);
		}
	}
	else {
		for (int i = 0; i <= cur->N-1; i++) {
			print_for_exam(cur->child[i]);
			printf("[%5d]\n", cur->key[i]);
		}
		print_for_exam(cur->child[cur->N]);
	}
}


void traverse(NODE* root, int depth)
{
	printf("\n");
	NODE* node = root;
	if (node->isLeaf) {
		for (int i = 0; i < depth; i++) {
			printf("\t\t\t||");
		}
		for (int vIdx = 0; vIdx < node->N; vIdx++) {
			printf("%6d [%6d]", node->key[vIdx],node->data[vIdx]);
		}

		//printf("\t---> : %p", node->Next);
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

	newNode->key   = (int*)malloc(sizeof(int) * MAX_DEGREE);
	newNode->data  = (int*)malloc(sizeof(int) * MAX_DEGREE);
	newNode->child = (NODE**)malloc(sizeof(NODE*) * MAX_DEGREE);

	newNode->N = 0;
	newNode->isLeaf = false;
	newNode->Next = NULL;

	return newNode;
}


//******INSERT*******//

void insert(NODE** root, int k, int data) {
	NODE* tmp = *root;

	if (((*root)->N) == MAX_DEGREE) {
		NODE* new_root = createNode();
		*root = new_root;
		new_root->N = 0;
		new_root->isLeaf = false;
		new_root->Next = NULL;

		new_root->child[0] = tmp;

		splitChild(new_root, 0);
		insertNonfull(new_root, k, data);
	}
	else {
		insertNonfull(*root, k, data);
	}
}


//내가 들어갈 노드가 너무 크면 반으로 나눠두고 내려간다.
//root의 주소는 바뀌지 않고, child만 반으로 쪼개지기 때문에 NODE *root로 인자를 받을 수 있다.
void splitChild(NODE* root, int into) {

	//NODE* right = (NODE*)malloc(sizeof(NODE*));
	NODE* right = createNode();
	NODE* left = root->child[into];
	right->isLeaf = left->isLeaf;
	left->Next = right;

	//내가 들어갈 노드가 리프이면? COPY UP
	if (left->isLeaf) {
		//일단 left와 right가 쪼개 갖는다! left는 t개, right 는 t-1개
		//key 나눠갖기
		for (int i = 0; i < DEGREE_t - 1; i++) {
			right->key[i] = left->key[DEGREE_t + i];
			right->data[i] = left->data[DEGREE_t + i];
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
			root->data[i] = root->data[i - 1];
			root->child[i + 1] = root->child[i];
		}
		//값 넣기 //******어떤값을 가져오느냐가 중요
		root->key[into] = left->key[DEGREE_t - 1];
		root->data[into] = left->data[DEGREE_t - 1];
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
			right->data[i] = left->data[DEGREE_t + i];
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
			root->data[i] = root->data[i - 1];
			root->child[i + 1] = root->child[i];
		}
		//값 넣기
		root->key[into] = left->key[DEGREE_t - 1];
		root->data[into] = left->data[DEGREE_t - 1];
		//값이 하나 늘었으니 갯수도 하나 증가
		root->N++;
		//child 연결하기
		root->child[into + 1] = right;
	}
}

//값을 넣을 준비가 된 꽉 차지 않은 노드에 값 넣기
void insertNonfull(NODE* root, int k, int data) {
	
	//리프이면 바로 넣는다.
	//넣을 자리 찾기
	if (root->isLeaf){

		int idx = (root->N);
		while (idx > 0 && root->key[idx] >= k)
			idx--;
		//뒤로 밀어주고
		for (int i = (root->N)-1; i>=idx; i--) {
			root->key[i + 1] = root->key[i];
			root->data[i + 1] = root->data[i];
		}
		//값을 넣어준다.
		root->key[idx] = k;
		root->data[idx] = data;
		root->N++;
	}
	//리프가 아니면, 리프까지 내려가서 넣어야지!
	//그럼 일단 내려가야 할 곳을 쳐다보고 0_0, 뚱뚱하면 split() 괜찮으면 바로 내려간다.
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
		insertNonfull(root->child[idx], k, data);
	}
}


//******************** DELETE *************************//
void deleteKey(NODE** root, int k)
{
	if ((*root)->isLeaf)
	{
		int idx = (*root)->N;
		while (idx > 0 && (*root)->key[idx-1] >= k)
			idx--;


		//찾았으면 idx를 덮어씌워주는 느낌으로 delete
		for (int i = idx; i < (*root)->N-1; i++) {
			(*root)->key[i] = (*root)->key[i + 1];
			(*root)->data[i] = (*root)->data[i + 1];
		}
		(*root)->N--;
	}
	else
	{
		int idx = (*root)->N;
		while (idx > 0 && (*root)->key[idx-1] >= k)
			idx--;

		NODE* target = (*root)->child[idx];

		//내려갈 곳이 뚱뚱한지 안한지 먼저 체크 
		//그 다음에 내려갈 곳이 리프인지 아닌지를 먼저 확인해야 한다.
		if (target->N < DEGREE_t)
		{
			//리프임
			if (target->isLeaf) {

				// key 가 젤 오른쪽에 존재한다.(왼쪽 형제에게 얻어오거나 합치기)
				if (idx == (*root)->N) {

					NODE* sibling = (*root)->child[idx - 1];

					//충분! 빌리기
					if (sibling->N >= DEGREE_t) {
						//target에 자리 만들어두기
						for (int i = target->N; i > 0; i--) {
							target->key[i] = target->key[i - 1];
							target->data[i] = target->data[i - 1];
						}
						for (int i = target->N; i >= 0; i--) {
							target->child[i + 1] = target->child[i];
						}
						//형제 마지막값 가져오기
						target->key[0] = sibling->key[sibling->N - 1];
						target->data[0] = sibling->data[sibling->N - 1];
						//형제 마지막자식 가져오기
						target->child[0] = sibling->child[sibling->N];

						target->N = target->N++;
						sibling->N = sibling->N--;

						//root->key[idx-1]에 값 넣어주기
						(*root)->key[idx - 1] = sibling->key[sibling->N - 1];
						(*root)->data[idx - 1] = sibling->data[sibling->N - 1];
					}
					//부족! 합치기(리프case: 부모키 가지고 오지 않고 그대로오오오 합치기)
					else {
						for (int i = 0; i < target->N; i++) {
							sibling->key[DEGREE_t - 1 + i] = target->key[i];
							sibling->data[DEGREE_t - 1 + i] = target->data[i];
						}
						sibling->N = sibling->N + target->N;
						sibling->Next = target->Next;
						//free(target);
						target = sibling;
						//ERROR 유발자일 것 같으니 나중에 해봅니다.
						//free(sibling);
						(*root)->N--;

						if ((*root)->N == 0) {
							//printf("\nROOT GOT CHANGED!!!!\n");
							(*root) = target;
						}
					}
				}
				// 오른쪽 형제랑 합칠 수 있는 모든 경우
				else
				{
					NODE* sibling = (*root)->child[idx + 1];

					//충분! 빌리기
					if (sibling->N >= DEGREE_t) {
						//형제 첫번째 값 가져오기
						target->key[target->N] = sibling->key[0];
						target->data[target->N] = sibling->data[0];
						target->child[target->N + 1] = sibling->child[0];
						target->N = target->N++;

						//siblig 한칸씩 앞으로 당겨오기
						//1) key
						for (int i = 0; i < sibling->N - 1; i++) {
							sibling->key[i] = sibling->key[i + 1];
							sibling->data[i] = sibling->data[i + 1];
						}
						//2) children
						for (int i = 0; i <= sibling->N - 1; i++)
							sibling->child[i] = sibling->child[i + 1];
						sibling->N = sibling->N--;

						//root->key[idx-1]에 값 넣어주기
						(*root)->key[idx] = target->key[target->N-1];
						(*root)->data[idx] = target->data[target->N - 1];
					}
					//부족! 합치기
					// 부모키 가지고 오지 않고 그대로오오오 합치기
					else {
						for (int i = 0; i < sibling->N; i++) {
							target->key[DEGREE_t -1 + i] = sibling->key[i];
							target->data[DEGREE_t - 1+ i] = sibling->data[i];
						}
						target->Next = sibling->Next;
						target->N = target->N + sibling->N;

						//부모값 하나씩 앞으로 당기기
						//for (int i = ((*root)->N) - 1; i > idx; i--)
						for (int i = idx; i < (*root)->N-1; i++) {
							(*root)->key[i] = (*root)->key[i+1];
							(*root)->data[i] = (*root)->data[i+1];
							(*root)->child[i+1] = (*root)->child[i+2];
						}
						(*root)->N--;


						if ((*root)->N == 0) {
							//printf("\nROOT GOT CHANGED!!!!\n");
							(*root) = target;
							//free(target);
						}
					}
				}
			}
			//리프아님
			else {

				// key 가 젤 오른쪽에 존재한다.(왼쪽 형제에게 얻어오거나 합치기)
				if (idx == (*root)->N) {

					NODE* sibling = (*root)->child[idx - 1];

					//충분! 빌리기
					if (sibling->N >= DEGREE_t) {
						//target에 자리 만들어두기
						for (int i = target->N; i > 0; i--) {
							target->key[i] = target->key[i - 1];
							target->data[i] = target->data[i - 1];
						}
						for (int i = target->N; i >= 0; i--) {
							target->child[i + 1] = target->child[i];
						}
						//부모값 가져오기
						target->key[0] = (*root)->key[idx - 1];
						target->data[0] = (*root)->data[idx - 1];
						//형제 마지막자식 가져오기
						target->child[0] = sibling->child[sibling->N];
						//root->key[idx-1]에 값 넣어주기
						(*root)->key[idx - 1] = sibling->key[sibling->N - 1];
						(*root)->data[idx - 1] = sibling->data[sibling->N - 1];

						target->N = target->N++;
						sibling->N = sibling->N--;

					}
					//부족! 합치기(not리프case: 부모키 가지고 내려오면서)
					else {
						sibling->key[DEGREE_t - 1] = (*root)->key[idx - 1];
						sibling->data[DEGREE_t - 1] = (*root)->data[idx - 1];
						for (int i = 0; i < target->N; i++) {
							sibling->key[DEGREE_t + i] = target->key[i];
							sibling->data[DEGREE_t + i] = target->data[i];
						}
						for (int i = 0; i <= target->N; i++) {
							sibling->child[DEGREE_t + 1 + i] = target->child[i];
						}
						sibling->N = sibling->N + 1 + target->N;
						sibling->Next = target->Next;
						target = sibling;
						//ERROR 유발자일 것 같으니 나중에 해봅니다.
						//free(sibling);
						(*root)->N--; //젤 오른쪽 값이니깐 키값이나 자식 당겨줄 필요없이 갯수만 하나 줄여준다.

						if ((*root)->N == 0) {
							//printf("\nROOT GOT CHANGED!!!!\n");
							(*root) = target;
						}
					}
				}
				// 오른쪽 형제랑 합칠 수 있는 모든 경우
				else
				{
					NODE* sibling = (*root)->child[idx + 1];

					//충분! 빌리기
					if (sibling->N >= DEGREE_t) {
						//부모값 가져오기
						target->key[target->N] = (*root)->key[idx];
						target->data[target->N] = (*root)->data[idx];
						//형제의 첫번째 값 부모 주기
						(*root)->key[idx] = sibling->key[0];
						(*root)->data[idx] = sibling->data[0];
						//형제의 첫번째 자식 데려오기
						target->child[target->N + 1] = sibling->child[0];
						target->N++;

						//siblig 한칸씩 앞으로 당겨오기
						//1) key
						for (int i = 0; i < sibling->N - 1; i++) {
							sibling->key[i] = sibling->key[i + 1];
							sibling->data[i] = sibling->data[i + 1];
						}
						//2) children
						for (int i = 0; i <= sibling->N - 1; i++)
							sibling->child[i] = sibling->child[i + 1];
						sibling->N--;

					}
					//부족! 합치기
					else {
						target->key[DEGREE_t-1] = (*root)->key[idx];
						target->data[DEGREE_t-1] = (*root)->data[idx];
						for (int i = 0; i < sibling->N; i++) {
							target->key[DEGREE_t + i] = sibling->key[i];
							target->data[DEGREE_t + i] = sibling->data[i];
						}
						for (int i = 0; i <= sibling->N; i++) {
							target->child[DEGREE_t + 1 + i] = sibling->child[i];
						}
						target->Next = sibling->Next;
						target->N = target->N + 1 + sibling->N;

						//부모값 하나씩 앞으로 당기기
						for (int i = idx; i< (*root)->N-1; i++) {
							(*root)->key[i] = (*root)->key[i+1];
							(*root)->data[i] = (*root)->data[i+1];
							(*root)->child[i+1] = (*root)->child[i+2];
						}
						(*root)->N--;


						if ((*root)->N == 0) {
							//printf("\nROOT GOT CHANGED!!!!\n");
							(*root) = target;
							//free(target);
						}
					}
				}
			}

		}

		deleteKey(&target, k);
	}	
}