/*
* tiny.c - A simple, iterative HTTP/1.0 Web server that uses the
* GET method to serve static and dynamic content
*/
#include "csapp.h"
void doit(int fd);
void read_requesthdrs(rio_t *rp);
int parse_uri(char *uri, char *filename, char *cgiargs);
void serve_static(int fd, char *filename, int filesize);
void get_filetype(char *filename, char *filetype);
void serve_dynamic(int fd, char *filename, char *cgiargs);
void clienterror(int fd, char *cause, char *errnum, char *shortmsg, char *longmsg);
void verEcho(int fd);

int main(int argc, char **argv)
{
    int listenfd, connfd;
    char hostname[MAXLINE], port[MAXLINE];
    socklen_t clientlen;
    struct sockaddr_storage clientaddr;

    //인자가 두개가 아니면 에러 메시지 반환
    /* Check command-line args */
    if (argc != 2)
    {
        fprintf(stderr, "usage: %s <port>\n", argv[0]);
        exit(1);
    }

    //listenfd가 생성되고,
    listenfd = Open_listenfd(argv[1]);
    while (1)
    {
        clientlen = sizeof(clientaddr);
        connfd = Accept(listenfd, (SA *)&clientaddr, &clientlen);
        Getnameinfo((SA *)&clientaddr, clientlen, hostname, MAXLINE, port, MAXLINE, 0);
        printf("Accepted connection from (%s, %s)\n", hostname, port);

        // echo(connfd);
        doit(connfd);
        // verEcho(connfd);
        Close(connfd);
    }
}

// void verEcho(int fd)
// {
//     int is_static;
//     struct stat sbuf;
//     char buf[MAXLINE], method[MAXLINE], uri[MAXLINE], version[MAXLINE];
//     char filename[MAXLINE], cgiargs[MAXLINE];
//     rio_t rio;

//     /* Read request line and headers */
//     Rio_readinitb(&rio, fd);
//     Rio_readlineb(&rio, buf, MAXLINE);
//     printf("Request headers:\n");
//     printf("%s", buf);
//     sscanf(buf, "%s %s %s", method, uri, version);

//     printf(">>>>>>>>HTTP version: %s<<<<<<<\n", version);
//     strcpy(buf, version);
    
//     Rio_writen(fd, buf, strlen(buf));
// }


void doit(int fd)
{
    int is_static;
    struct stat sbuf;
    char buf[MAXLINE], method[MAXLINE], uri[MAXLINE], version[MAXLINE];
    char filename[MAXLINE], cgiargs[MAXLINE];
    rio_t rio;

    /* Read request line and headers */
    Rio_readinitb(&rio, fd);
    Rio_readlineb(&rio, buf, MAXLINE);
    printf("Request headers:\n");
    printf("%s", buf);
    sscanf(buf, "%s %s %s", method, uri, version);

    printf(">>>>>>>>HTTP version: %s<<<<<<<\n", version);


    //HEAD method 추가하기
    if(!strcasecmp(method, "HEAD"))
    {        
        char buf[MAXLINE];
        /* Send response headers to client */
        sprintf(buf, "HTTP/1.0 200 OK\r\n");
        sprintf(buf, "%sServer: Tiny Web Server\r\n", buf);
        sprintf(buf, "%sConnection: close\r\n", buf);
        Rio_writen(fd, buf, strlen(buf));
        printf("Response headers:\n");
        printf("%s", buf);

        return;
    }

    if (strcasecmp(method, "GET"))// original src code
    {
        clienterror(fd, method, "501", "Not implemented",
                    "Tiny does not implement this method");
        return;
    }

    
    read_requesthdrs(&rio);

    /* Parse URI from GET request */
    //클라이언트가 요청하는 파일이 static인지 dynamic인지 판단
    is_static = parse_uri(uri, filename, cgiargs);
    // 해당 파일이 디스크 안에 없으면 에러 반환
    if(stat(filename, &sbuf) < 0)
    {
        clienterror(fd, filename, "404", "Not found",
                    "Tiny couldn’t find this file");
        return;
    }

    if (is_static)
    { /* Serve static content */
        // 보통 파일인지 읽기 권한이 있는지 확인하는 
        if (!(S_ISREG(sbuf.st_mode)) || !(S_IRUSR & sbuf.st_mode))
        {
            clienterror(fd, filename, "403", "Forbidden",
                        "Tiny couldn’t read the file");
            return;
        }
        serve_static(fd, filename, sbuf.st_size);
    }
    else
    { /* Serve dynamic content */
        // 보통 파일인지 읽기 권한이 있는지 확인하는 
        if (!(S_ISREG(sbuf.st_mode)) || !(S_IXUSR & sbuf.st_mode))
        {
            clienterror(fd, filename, "403", "Forbidden",
                        "Tiny couldn’t run the CGI program");
            return;
        }
        serve_dynamic(fd, filename, cgiargs);
    }
}

void clienterror(int fd, char *cause, char *errnum, char *shortmsg, char *longmsg)
{
    char buf[MAXLINE], body[MAXBUF];
    /* Build the HTTP response body */
    sprintf(body, "<html><title>Tiny Error</title>");
    sprintf(body, "%s<body bgcolor="
                  "ffffff"
                  ">\r\n",
            body);
    sprintf(body, "%s%s: %s\r\n", body, errnum, shortmsg);
    sprintf(body, "%s<p>%s: %s\r\n", body, longmsg, cause);
    sprintf(body, "%s<hr><em>The Tiny Web server</em>\r\n", body);

    /* Print the HTTP response */
    sprintf(buf, "HTTP/1.0 %s %s\r\n", errnum, shortmsg);
    Rio_writen(fd, buf, strlen(buf));
    sprintf(buf, "Content-type: text/html\r\n");
    Rio_writen(fd, buf, strlen(buf));
    sprintf(buf, "Content-length: %d\r\n\r\n", (int)strlen(body));
    Rio_writen(fd, buf, strlen(buf));
    Rio_writen(fd, body, strlen(body));
}

void read_requesthdrs(rio_t *rp)
{
    char buf[MAXLINE];
    //rp(rio pointer)부터 maxline만큼 읽어서 buf로 복사한다.
    Rio_readlineb(rp, buf, MAXLINE);
    while (strcmp(buf, "\r\n"))
    {
        Rio_readlineb(rp, buf, MAXLINE);
        printf("%s", buf);
    }
    return;
}

int parse_uri(char *uri, char *filename, char *cgiargs)
{
    char *ptr;
    if (!strstr(uri, "cgi-bin"))
    { /* Static content */
        strcpy(cgiargs, "");
        strcpy(filename, ".");
        strcat(filename, uri);
        if (uri[strlen(uri) - 1] == '/')
            strcat(filename, "home.html");
            // strcat(filename, "complete.mp4");
        return 1;
    }
    else
    { /* Dynamic content */
        ptr = index(uri, '?');
        if (ptr)
        {
            strcpy(cgiargs, ptr + 1);
            *ptr = '\0';
        }
        else
            strcpy(cgiargs, "");
        strcpy(filename, ".");
        strcat(filename, uri);
        return 0;
    }
}

void serve_static(int fd, char *filename, int filesize)
{
    int srcfd;
    char *srcp, filetype[MAXLINE], buf[MAXBUF];
    /* Send response headers to client */
    get_filetype(filename, filetype);
    sprintf(buf, "HTTP/1.0 200 OK\r\n");
    sprintf(buf, "%sServer: Tiny Web Server\r\n", buf);
    sprintf(buf, "%sConnection: close\r\n", buf);
    sprintf(buf, "%sContent-length: %d\r\n", buf, filesize);
    sprintf(buf, "%sContent-type: %s\r\n\r\n", buf, filetype);
    Rio_writen(fd, buf, strlen(buf));
    printf("Response headers:\n");
    printf("%s", buf);

    /* Send response body to client */
    srcfd = Open(filename, O_RDONLY, 0);
    // Original code
    srcp = Mmap(0, filesize, PROT_READ, MAP_PRIVATE, srcfd, 0);
    
    
    //Excercise 11.9
    // char* srcbuf;
    // srcbuf = Malloc(filesize);
    // fd --> buffer
    // Rio_readn(srcfd, srcbuf, sizeof(srcbuf));
    
    Close(srcfd);
    Rio_writen(fd, srcp, filesize); //original code
    // Rio_writen(fd, srcbuf, filesize);
    Munmap(srcp, filesize);
    // free(srcbuf);
}

/*
 * get_filetype - Derive file type from filename
 */
void get_filetype(char *filename, char *filetype)
{
    if (strstr(filename, ".html"))
        strcpy(filetype, "text/html");
    else if (strstr(filename, ".gif"))
        strcpy(filetype, "image/gif");
    else if (strstr(filename, ".png"))
        strcpy(filetype, "image/png");
    else if (strstr(filename, ".jpg"))
        strcpy(filetype, "image/jpeg");
    // else if (strstr(filename, ".mpeg"))
    //     strcpy(filetype, "video/mpeg");
    // else if (strstr(filename, ".avi"))
    //     strcpy(filetype, "video/avi");
    else if (strstr(filename, ".mp4"))
        strcpy(filetype, "video/mpeg");
    else
        strcpy(filetype, "text/plain");
}

void serve_dynamic(int fd, char *filename, char *cgiargs)
{
    char buf[MAXLINE], *emptylist[] = {NULL};
    /* Return first part of HTTP response */
    sprintf(buf, "HTTP/1.0 200 OK\r\n");
    Rio_writen(fd, buf, strlen(buf));
    sprintf(buf, "Server: Tiny Web Server\r\n");
    Rio_writen(fd, buf, strlen(buf));

    if (Fork() == 0)
    { /* Child */
        /* Real server would set all CGI vars here */
        setenv("QUERY_STRING", cgiargs, 1);
        Dup2(fd, STDOUT_FILENO);              /* Redirect stdout to client */
        Execve(filename, emptylist, environ); /* Run CGI program */
    }
    Wait(NULL); /* Parent waits for and reaps child */
}