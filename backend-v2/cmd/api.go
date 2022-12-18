package main

import (
	"cloud.google.com/go/firestore"
	"context"
	"fmt"
	"github.com/99designs/gqlgen/graphql/handler"
	"github.com/99designs/gqlgen/graphql/playground"
	"github.com/peppys/service-template/gen/go/graphql"
	"github.com/peppys/service-template/internal/config"
	"github.com/peppys/service-template/internal/graphqlresolvers"
	"google.golang.org/api/option"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"io"
	"log"
	"net/http"
	"os"
)

var appConfig *config.AppConfig

func main() {
	appConfig = config.NewAppConfig()

	mux := http.NewServeMux()

	// graphql
	mux.Handle("/graphql", handler.NewDefaultServer(
		graphql.NewExecutableSchema(
			graphql.Config{Resolvers: graphqlresolvers.New()}),
	))
	mux.Handle("/graphiql", playground.Handler("GraphQL playground", "/graphql"))

	log.Fatal(listenChanges(context.Background(), os.Stdout, "personal-site-staging-a449f", "songs"))

	//server := &http.Server{Addr: ":8080", Handler: mux}
	//log.Println("Listing on port :8080...")
	//log.Fatal(server.ListenAndServe())
}

// listenChanges listens to a query, returning the list of document changes.
func listenChanges(ctx context.Context, w io.Writer, projectID, collection string) error {
	serviceAccountJson := os.Getenv("GOOGLE_SERVICE_ACCOUNT_KEY_JSON")
	//serviceAccountJson = strings.ReplaceAll(serviceAccountJson, "'", "")

	client, err := firestore.NewClient(ctx, projectID, option.WithCredentialsJSON([]byte(serviceAccountJson)))
	if err != nil {
		return fmt.Errorf("firestore.NewClient: %v", err)
	}

	defer client.Close()

	it := client.Collection(collection).Snapshots(ctx)
	for {
		snap, err := it.Next()
		// DeadlineExceeded will be returned when ctx is cancelled.
		if status.Code(err) == codes.DeadlineExceeded {
			return nil
		}
		if err != nil {
			return fmt.Errorf("Snapshots.Next: %v", err)
		}
		if snap != nil {
			for _, change := range snap.Changes {
				switch change.Kind {
				case firestore.DocumentAdded:
					fmt.Fprintf(w, "New song: %v\n", change.Doc.Data())
				case firestore.DocumentModified:
					fmt.Fprintf(w, "Modified song: %v\n", change.Doc.Data())
				case firestore.DocumentRemoved:
					fmt.Fprintf(w, "Removed song: %v\n", change.Doc.Data())
				}
			}
		}
	}
}
