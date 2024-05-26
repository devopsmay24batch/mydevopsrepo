# Define variables

variable "example_string" {
  type    = string
  default = "Hello, Terraform!"
}

variable "example_number" {
  type    = number
  default = 42
}

variable "example_bool" {
  type    = bool
  default = true
}

variable "example_list" {
  type    = list(string)
  default = ["apple", "banana", "cherry"]
}

variable "example_map" {
  type = map(string)
  default = {
    name = "John"
    age  = "30"
  }
}

variable "example_set" {
  type    = set(string)
  default = ["one", "two", "three"]
}

variable "example_object" {
  type = object({
    id    = number
    name  = string
    tags  = map(string)
  })
  default = {
    id    = 1
    name  = "Terraform"
    tags  = {
      environment = "dev"
      project     = "terraform_tutorial"
    }
  }
}

variable "example_tuple" {
  type = tuple([string, number, bool])
  default = ["Terraform", 1, true]
}

variable "example_string_to_encode" {
  type    = string
  default = "Hello, World!"
}

variable "example_null_string" {
  type    = string
  default = null
}

variable "list1" {
  type    = list(string)
  default = ["one", "two"]
}

variable "list2" {
  type    = list(string)
  default = ["three", "four"]
}

variable "nested_list" {
  type    = list(list(string))
  default = [["one", "two"], ["three", "four"]]
}

variable "map1" {
  type = map(string)
  default = {
    name = "John"
  }
}

variable "map2" {
  type = map(string)
  default = {
    age = "30"
  }
}

variable "example_split_string" {
  type    = string
  default = "apple,banana,cherry"
}
