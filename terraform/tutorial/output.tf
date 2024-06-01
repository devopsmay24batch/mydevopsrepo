# Outputs for variables

output "example_string_output" {
  value = var.example_string
}

output "example_number_output" {
  value = var.example_number
}

output "example_bool_output" {
  value = var.example_bool
}

output "example_list_output" {
  value = var.example_list
}

output "example_map_output" {
  value = var.example_map
}

output "example_set_output" {
  value = var.example_set
}

output "example_object_output" {
  value = var.example_object
}

output "example_tuple_output" {
  value = var.example_tuple
}

# Outputs for functions

output "example_list_length" {
  value = length(var.example_list)
}

output "joined_string" {
  value = join(", ", var.example_list)
}

output "split_list" {
  value = split(",", var.example_split_string)
}

output "lookup_example" {
  value = lookup(var.example_map, "name", "default_name")
}

output "concat_example" {
  value = concat(var.list1, var.list2)
}

output "merge_example" {
  value = merge(var.map1, var.map2)
}

output "file_content" {
  value = file("example.txt")
}

output "base64_encoded" {
  value = base64encode(var.example_string_to_encode)
}

output "base64_decoded" {
  value = base64decode(base64encode(var.example_string_to_encode))
}
