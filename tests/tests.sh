#!/usr/bin/env bats

@test "login" {
  run python3 -m recodex_cli login --username test --password test --api-url http://localhost:8081
  [ "$status" -eq 0 ]
}

@test "call groups.default" {
  # check that the response returns the group uuid
  local expected_uuid="10000000-2000-4000-8000-160000000000"

  run python3 -m recodex_cli call groups.default
  [ "$status" -eq 0 ]
  [[ "$output" =~ "$expected_uuid" ]]
}

@test "upload file" {
  # check that the response contains the file uuid
  local expected_uuid="10000000-2000-4000-8000-160000000000"

  run python3 -m recodex_cli file upload tests/utils/uploadTestFile.txt 
  [ "$status" -eq 0 ]
  [[ "$output" =~ "$expected_uuid" ]]
}

@test "failed validation" {
  # the command has a too long 'locale' parameter
  run python3 -m recodex_cli call registration.create_invitation --body '{"email":"name@domain.tld","firstName":"text","lastName":"text","instanceId":"10000000-2000-4000-8000-160000000000","titlesBeforeName":"text","titlesAfterName":"text","groups":["string"],"locale":"THIS TEXT IS TOO LONG","ignoreNameCollision":true}' 
  
  [ "$status" -ne 0 ]
  # check that the parameter was identified as too long
  [[ "$output" =~ "'THIS TEXT IS TOO LONG' is too long" ]]
}

@test "passed validation" {
  # the same command as in the 'failed validation' test but with corrected 'locale'
  run python3 -m recodex_cli call registration.create_invitation --body '{"email":"name@domain.tld","firstName":"text","lastName":"text","instanceId":"10000000-2000-4000-8000-160000000000","titlesBeforeName":"text","titlesAfterName":"text","groups":["string"],"locale":"en","ignoreNameCollision":true}' 
  [ "$status" -eq 0 ]
}

@test "logout" {
  run python3 -m recodex_cli logout
  [ "$status" -eq 0 ]
}

# after logout, it should no longer be possible to call endpoints
@test "failed call groups.default" {
  run python3 -m recodex_cli call groups.default
  [ "$status" -ne 0 ]
}
