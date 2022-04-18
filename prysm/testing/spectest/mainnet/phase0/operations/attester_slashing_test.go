package operations

import (
	"testing"

	"github.com/prysmaticlabs/prysm/testing/spectest/shared/phase0/operations"
)

func TestMainnet_Phase0_Operations_AttesterSlashing(t *testing.T) {
	operations.RunAttesterSlashingTest(t, "mainnet")
}
