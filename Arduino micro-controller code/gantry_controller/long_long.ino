long long char_to_LL(char *str){
  /* converts character array to long long int */
  long long result = 0; // Initialize result
  // Iterate through all characters of input string and update result
  for (int i = 0; str[i] != '\0'; ++i)
    result = result*10 + str[i] - '0';
  return result;
}

void LL_to_Serial(long long ll){
  /* prints long long int variable over serial */
  uint64_t xx = ll/1000000000ULL;
  if (xx >0) Serial.print((long)xx);
  Serial.print((long)(ll-xx*1000000000));
}
