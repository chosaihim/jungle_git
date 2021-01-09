#include <stdio.h>
#include <stdlib.h>

typedef struct _NODE{
    int data;

    struct _NODE *left;
    struct _NODE *right;

}NODE;

NODE* root = NULL;

NODE* createNode(int data){
    NODE* new = malloc(sizeof(NODE));
    new->left  = NULL;
    new->right = NULL;

    return new;
}

void deleteNode(NODE* node){
    free(node);
}

NODE* BST_insert(NODE* root, int data)
{
    if(root == NULL) //빈 노드면 그 자리를 채운다.
    {
        root = (NODE*)malloc(sizeof(NODE));
        root->left = root->right = NULL;
        root->data = data;
        return root;
    }
    else
    {
        if(root->data > data)
            root->left  = BST_insert(root->left,data);
        else
            root->right = BST_insert(root->right,data); 
    }

    return root;
    
}

NODE* findMinNode(NODE* root){
    NODE* tmp = root;
    while(tmp->left != NULL)
        tmp = tmp->left;
    return tmp;
}

NODE* BST_delete(NODE *root, int data){
    
    NODE* tNode = NULL;
    if(root == NULL) return NULL;

    //일단 지우려는 data가 있는 node를 찾아간다!
    if(root->data > data)                                   //해당 노드가 내 값보다 크면 왼쪽으로
        root->left = BST_delete(root->left, data);
    else if(root->data < data)                              //해당 노드가 내 값보다 작으면 오른쪽으로
        root->right = BST_delete(root->right, data);
    else                                                    //값을 찾았으면 이제 지우기 시작!
    {
        //자식 노드가 둘다 있을 경우: 오른쪽 sub tree의 가장 왼쪽 값을 찾아서 교체해주면 됨
        if(root->left != NULL && root->right != NULL){
            
            tNode = findMinNode(root->right);                       //오른쪽 sub tree에서 젤 왼쪽값을 찾아준다.
            root->data = tNode->data;                               //그 노드로 데이터를 바꿔낀다. node 자체의 물리적 공간을 삭제해 주는게 아니라 값만 갈아낌
            root->right = BST_delete(root->right, tNode->data);     //갖다 쓴 그 노드를 지우러간다.
        }

        //자식 노드가 하나만 있을 경우: 그냥 지우고 밑에 달려있던 노드 끌고 올라오면 됨
        else{
            tNode = (root->left == NULL) ? root->right : root->left;
            free(root);
            return tNode;
        }
    }

    return root;
}

NODE* BST_search(NODE* root, int data)
{
    if(root==NULL) return NULL;

    if(root->data > data) return BST_search(root->left, data);
    else return BST_search(root->right, data);
}

void BST_print(NODE* root)
{
    if(root == NULL)
        return;

    printf("%d ", root->data);
    BST_print(root->left);
    BST_print(root->right);
}

void child_print(NODE* root)
{
    if(root == NULL) return;

    if(root->left) printf("%d ", root->left->data);
    if(root->right) printf("%d ", root->right->data);
    
    child_print(root->left);
    child_print(root->right);
}

int main()
{
    root = BST_insert(root, 5);
    root = BST_insert(root, 3);
    root = BST_insert(root, 7);
    root = BST_insert(root, 1);
    root = BST_insert(root, 9);
    root = BST_insert(root, 6);

    root = BST_delete(root, 7);

    BST_print(root);
    // child_print(root);
}