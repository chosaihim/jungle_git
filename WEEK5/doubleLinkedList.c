#include <stdio.h>
#include <stdlib.h> 


typedef struct listNode{
    int Data;
    struct listNode* Next;
    struct listNode* Prev;
}Node;

Node* createNode(int data){
    Node* newNode = (Node*)malloc(sizeof(Node));

    //variable inialization
    newNode->Data = data;
    newNode->Next = NULL;
    newNode->Prev = NULL;

    return newNode;
}

void deleteNode(Node* node){
    free(node);
}

Node* getNodeAt(Node* head, int index){

    Node* horse = head;
    int count = 0;

    while(horse != NULL){
        if(count++ == index){
            return horse;
        }
        horse = horse->Next;
    }

    return NULL;
}

int countNode(Node* head){  //list에 총 노드가 몇개인지 
    int count = 0;
    Node* horse = head;

    while(horse != NULL){
        horse = horse->Next;
        count++;
    }
    return count;
}

void addNode(Node** head, Node* newNode){ //call by address
   
    //no list exists
    if((*head) == NULL){
        *head = newNode;
    }

    //list exists
    else{
        Node *horse = (*head);

        while(horse->Next != NULL){
            horse = horse->Next;
        }

        horse->Next = newNode;
        newNode->Prev = horse; 
    }

}

void insertAfter(Node* Current, Node* newNode){
    
    //head
    if(Current->Prev == NULL && Current->Next == NULL){//is current Node head?
        Current->Next = newNode;
        newNode->Prev = Current;
    }
    
    else{
    // not head
        //if tail
        if(Current->Next == NULL){
            Current->Next = newNode;
            newNode->Prev = Current;
        }

        //in the middle of 2 nodes
        else{
            Current->Next->Prev = newNode;
            newNode->Prev = Current;
            newNode->Next = Current->Next;
            Current->Next = newNode;            
        }
    }
}

void removeNode(Node **head, Node* remove){
    
    //head
    if(*head == remove){
        *head = remove->Next; // head는 계속 tracking 해야 하니깐, 지우기전에 다음 node로 넘겨줌
    }
    
    //when remove has next link to go
    if(remove->Next != NULL){
        remove->Next->Prev = remove->Prev;
    }

    //when remove has prev link to go
    if(remove->Prev != NULL){
        remove->Prev->Next = remove->Next;
    }

    deleteNode(remove);
    
}

int main(){
    int i = 0;
    int count = 0;

    //future head
    Node* List = NULL;

    //tmep Node
    Node* newNode = NULL;

    //current Node
    Node* Curr = NULL;

    for(i =0; i<5; i++){
        newNode = createNode(i);
        addNode(&List, newNode);
    }
    
    count = countNode(List);
    for(i=0; i<count; i++){
        Curr = getNodeAt(List, i);
        printf("List(%d)= %d\n", i, Curr->Data);
    }



    printf("-------------5 nodes created --------------\n");

    newNode = createNode(99);
    Curr = getNodeAt(List,0);
    insertAfter(Curr,newNode);

    newNode = createNode(444);
    Curr = getNodeAt(List,4);
    insertAfter(Curr,newNode);
    
    count = countNode(List);
    for(i=0; i<count; i++){
        Curr = getNodeAt(List, i);
        printf("List(%d)= %d\n", i, Curr->Data);
    }

    printf("-------------After 2 node inserted--------------\n");

    newNode = getNodeAt(List,1);
    removeNode(&List, newNode);

    newNode = getNodeAt(List,0);
    removeNode(&List, newNode);

    
    count = countNode(List);
    for(i=0; i<count; i++){
        Curr = getNodeAt(List, i);
        printf("List(%d)= %d\n", i, Curr->Data);
    }

    printf("-------------After Noe with index 1 removed--------------\n");

    return 0;

}