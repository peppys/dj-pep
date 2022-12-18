# backend for dj-pep

## Setup
#### Dependencies
- [docker](https://www.docker.com/) - containerizes application
- [gqlgen](https://github.com/99designs/gqlgen) - golang library for building GraphQL servers

### Installation
```shell script
# install docker
$ brew install docker

# install the tools listed in tools/tools.go
$ go install \ 
  github.com/99designs/gqlgen \
  # ... etc  
  
# generate graphql code from schema
$ gqlgen generate
```

#### Spin up the API
```shell script
docker-compose up -d
```


#### GraphQL
##### Navigate to http://localhost:8080/graphiql to interact with the GraphQL playground
```graphql
mutation Signup {
  signup(
    input: {
        email: "pep@test.com", 
        username: "pepsmooth", 
        password: "mypass", 
        givenName: "Pep", 
        familyName: "Smooth"
    }
  ) {
    accessToken
    refreshToken
    tokenType
    expires
  }
}
```
