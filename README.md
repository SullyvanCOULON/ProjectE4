# ProjectE4
LLM Agent dedicated to road safety

How is it composed ?

There is two version of this program :
  – One with the frontend and backend connected but with an hallucinating LLM (main and API_functionnal branch)
  - An other with no interface but a really effective LLM (rag branch)

How to use it ?

This program run with Python 1.13. Please make sure to install it before any use !
For each of these versions here is the procedure to follow :
  - For the interface you have to install the last version of Vue.js and Node.js
  - To use Docker, you have to install it
  - To run the program follow this instructions :
      - Write in the console "pip install -r "./requirement.txt"
      - Then write "pip install torch==2.7.0+cu118 --index-url https://download.pytorch.org/whl/cu118"
      - Then if you want to run the interface go to the right directory with "cd ./interface" and type "npm run dev"
      - If you want to run the code type "python ./RAG/RAGMultimodal.py"
   
This are the authors of this program :
Nathan LECOIN, Esteban NABONNE, Sullyvan COULON, Louka MORANDI
