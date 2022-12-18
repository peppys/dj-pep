package graphqlresolvers

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	graphql1 "github.com/peppys/service-template/gen/go/graphql"
)

func (r *mutationResolver) Placeholder(ctx context.Context) (bool, error) {
	return true, nil
}

func (r *queryResolver) Livez(ctx context.Context) (bool, error) {
	return true, nil
}

func (r *queryResolver) Readyz(ctx context.Context) (bool, error) {
	// TODO - check DB connection
	return true, nil
}

// Mutation returns graphql1.MutationResolver implementation.
func (r *Resolver) Mutation() graphql1.MutationResolver { return &mutationResolver{r} }

// Query returns graphql1.QueryResolver implementation.
func (r *Resolver) Query() graphql1.QueryResolver { return &queryResolver{r} }

type mutationResolver struct{ *Resolver }
type queryResolver struct{ *Resolver }
