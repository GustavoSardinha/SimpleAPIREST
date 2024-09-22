from django.shortcuts import render, get_object_or_404
from .models import Pessoa
from django.http import JsonResponse, Http404, HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PessoaForm
from django.views.decorators.csrf import csrf_exempt
import json

def pessoas(request):
    try:
        pessoas = Pessoa.objects.all().values()
        itens_por_pagina = 1
        pagina = request.GET.get('pagina', 1)
        paginator = Paginator(pessoas, itens_por_pagina)

        try:
            pessoas_paginadas = paginator.page(pagina)
        except PageNotAnInteger:
            pessoas_paginadas = paginator.page(1)
        except EmptyPage:
            pessoas_paginadas = paginator.page(paginator.num_pages)

        pessoas_list = list(pessoas_paginadas)

        return JsonResponse({
            "pessoas": pessoas_list,
            "paginacao": {
                "pagina_atual": pessoas_paginadas.number,
                "total_paginas": paginator.num_pages,
                "total_pessoas": paginator.count,
                "proxima_pagina": pessoas_paginadas.has_next(),
                "pagina_anterior": pessoas_paginadas.has_previous()
            }
        }, safe=False, status=200)

    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)

def pessoa_por_id(request, pessoa_id):
    try:
        pessoa = get_object_or_404(Pessoa, id=pessoa_id)
        pessoa_dic= {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'sobrenome': pessoa.sobrenome,
            'data+nascimento': pessoa.data_nascimento,
        }
        return JsonResponse(pessoa_dic)
    except Http404:
        return HttpResponseNotFound({"Nenhuma pessoa foi encontrada com esse id"})
    except Exception as e:
        return JsonResponse({"erro": e}, status=500)
@csrf_exempt
def criar_pessoa(request):
    try:
        if request.method == 'POST':
            form = PessoaForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({"sucesso": "Pessoa criada com sucesso!"}, status=201)
            else:
                return JsonResponse({"erro": form.errors}, status=400)  
        else:
            return JsonResponse({"erro": "Método não permitido. Use POST."}, status=405)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)
    
@csrf_exempt
def remove_pessoa(request, pessoa_id):
    try:
        if request.method == 'DELETE':
            pessoa = get_object_or_404(Pessoa, id=pessoa_id)
            pessoa.delete()
            return JsonResponse({"successo": "Pessoa removida com sucesso!"}, status=200)
        else:
            return JsonResponse({"erro": "Método não permitido. Use DELETE."}, status=405)
    except Http404:
        return JsonResponse({"erro": "Pessoa não encontrada."}, status=404)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)
    
@csrf_exempt
def atualiza_pessoa(request, pessoa_id):
    try:
        if request.method == 'PUT':
            pessoa = get_object_or_404(Pessoa, id=pessoa_id)
            dados = json.loads(request.body)
            for campo, valor in dados.items():
                if hasattr(pessoa, campo):
                    setattr(pessoa, campo, valor)
                else:
                    return JsonResponse({"erro": "Campo "+ campo + " inexistente"}, status=400)  
            pessoa.save()
            return JsonResponse({"sucesso": "Pessoa atualizada com sucesso!"}, status=200)
        else:
            return JsonResponse({"erro": "Método não permitido. Use PUT."}, status=405)

    except Http404:
        return JsonResponse({"erro": "Pessoa não encontrada."}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"erro": "Formato de dados inválido. Use JSON."}, status=400)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)