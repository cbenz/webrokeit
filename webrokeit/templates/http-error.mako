## -*- coding: utf-8 -*-


<%inherit file="/site.mako"/>


<%block name="container_content">
<div class="alert alert-block alert-error">
  <h4 class="alert-heading">${title}</h4>
  <p>${explanation}</p>
% if comment:
  <p>${comment}</p>
% endif
% if message:
  <p>${message}</p>
% endif
</div>
</%block>


<%block name="title_content">
${title} - ${parent.title_content()}
</%block>
