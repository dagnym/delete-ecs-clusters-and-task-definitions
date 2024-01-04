# delete-ecs-clusters-and-task-definitions

After my AWS account was compromised, and thousands of ECS clusters/task definitions were added to my account (racking up $400 of charges within a few weeks), I needed a solution for deleting them quickly - otherwise I would have to manually delete them one-by-one. Unfortunately, AWS support was not able to help me, so through some quick trial and error, I managed to create this Python script.

This script is run through the AWS cli, iterates through all listed regions on the AWS account and will:

  1) delete all ECS services
  2) deregister and then delete all task definitions
  3) delete all clusters 

ONLY USE THIS SCRIPT IF YOU WANT ALL OF THE ABOVE TO BE DELETED - you will need an alternative solution if you need to protect some clusters/definitions.

Also worth noting is the fact that you may need to change the "regions" array to suit the active/compromised regions on your AWS account.

I hope this helps others who have faced the unfortunate reality of a compromised AWS account. 
