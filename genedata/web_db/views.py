# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

import xml.dom.minidom as mini_dom

#importing all project functions
import gene_interaction.gene_interaction.interactions as gene_interaction
import gene_info.gene_info.info as gene_info
import patient_info.patient_info.info as patient_info

def index(request):
    if request.method == 'POST':
        context = {}
        if 'gene-interaction' in request.POST:
            gene = request.POST.get('gene')
            order = request.POST.get('order')
            #query_result = gene_interaction.query(gene,order)
            query_result = [{'g.id': 2, 'n_order_gene.id': 2806}, {'g.id': 2, 'n_order_gene.id': 3206}, {'g.id': 2, 'n_order_gene.id': 4612}, {'g.id': 2, 'n_order_gene.id': 5268}]
            context["query"] = gene
            context["result"] = query_result
            return render(request, 'web_db/gene_interaction.html', context)
        elif 'gene-statistics' in request.POST:
            gene = request.POST.get('gene')
            #query_result = gene_stat.query(gene)
            query_result = [{"mean": 2, "std": 3}, {"mean": 5, "std": 7}, {"mean": 11, "std": 13}, {"mean": 17, "std": 19}, {"mean": 23, "std": 27}, {"mean": 31, "std": 37}] 
            context["query"] = gene
            context["result"] = query_result
            return render(request, 'web_db/gene_stats.html', context)
        elif 'gene-information' in request.POST:
            gene = request.POST.get('gene')
            query_result = gene_info.query_gene(gene)
            context["query"] = gene
            context["symbol"] = query_result[0]["gene_symbol"]
            context["name"] = query_result[0]["gene_name"]
            context["result"] = query_result
            return render(request, 'web_db/gene_info.html', context)
        elif 'patient-information' in request.POST:
            patient = request.POST.get('patient')
            #context = patient_info.query(patient)
            context = {'gender': 'F', 'age': '57', 'education': 'PhD', 'id': 'X954_131107'}
            return render(request, 'web_db/patient_info.html', context)
        else:
            return render(request, 'web_db/index.html', context)
    else:
        return render(request, 'web_db/index.html')
