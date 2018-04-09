# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

import xml.dom.minidom as mini_dom

#importing all project functions
import gene_interaction.gene_interaction.interactions as gene_interaction
import gene_stats.gene_stats.stats as gene_stats
import gene_info.gene_info.info as gene_info
import patient_info.patient_info.info as patient_info

def index(request):
    if request.method == 'POST':
        context = {}
        if 'gene-interaction' in request.POST:
            gene = request.POST.get('gene')
            order = request.POST.get('order')
            query_result = gene_interaction.query(gene,order)
            context["order"] = order
            context["query"] = gene
            context["result"] = query_result
            return render(request, 'web_db/gene_interaction.html', context)
        elif 'gene-statistics' in request.POST:
            gene = request.POST.get('gene')
            query_result = gene_stats.query(gene)
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
            context = patient_info.query(patient)
            return render(request, 'web_db/patient_info.html', context)
        else:
            return render(request, 'web_db/index.html', context)
    else:
        return render(request, 'web_db/index.html')
