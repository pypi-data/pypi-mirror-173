#pragma once

#include <alpaqa/config/config.hpp>
#include <pybind11/gil.h>
namespace py = pybind11;

template <class ProblemBase>
class ProblemTrampoline : ProblemBase {
    USING_ALPAQA_CONFIG_TEMPLATE(ProblemBase::config_t);
    using ProblemBase::ProblemBase;

    // clang-format off
    real_t eval_f(crvec x) const override { py::gil_scoped_acquire acq; PYBIND11_OVERRIDE(real_t, ProblemBase, eval_f, x); }
    void eval_grad_f(crvec x, rvec grad_fx) const override { py::gil_scoped_acquire acq; PYBIND11_OVERRIDE(void, ProblemBase, eval_grad_f, x, grad_fx); }
    void eval_g(crvec x, rvec gx) const override { py::gil_scoped_acquire acq; PYBIND11_OVERRIDE(void, ProblemBase, eval_g, x, gx); }
    void eval_grad_g_prod(crvec x, crvec y, rvec grad_gxy) const override { py::gil_scoped_acquire acq; PYBIND11_OVERRIDE(void, ProblemBase, eval_grad_g_prod, x, y, grad_gxy); }
    void eval_grad_gi(crvec x, index_t i, rvec grad_gi) const override { py::gil_scoped_acquire acq; PYBIND11_OVERRIDE(void, ProblemBase, eval_grad_gi, x, i, grad_gi); }
    void eval_hess_L_prod(crvec x, crvec y, crvec v, rvec Hv) const override { py::gil_scoped_acquire acq; PYBIND11_OVERRIDE(void, ProblemBase, eval_hess_L_prod, x, y, v, Hv); }
    void eval_hess_L(crvec x, crvec y, rmat H) const override { py::gil_scoped_acquire acq; PYBIND11_OVERRIDE(void, ProblemBase, eval_hess_L, x, y, H); }
    // clang-format on

    // clang-format off
    real_t eval_f_grad_f(crvec x, rvec grad_fx) const override { py::gil_scoped_acquire acq; PYBIND11_OVERRIDE(real_t, ProblemBase, eval_f_grad_f, x, grad_fx); }
    real_t eval_f_g(crvec x, rvec g) const override { py::gil_scoped_acquire acq; PYBIND11_OVERRIDE(real_t, ProblemBase, eval_f_g, x, g); }
    real_t eval_f_grad_f_g(crvec x, rvec grad_fx, rvec g) const override { py::gil_scoped_acquire acq; PYBIND11_OVERRIDE(real_t, ProblemBase, eval_f_grad_f_g, x, grad_fx, g); }
    void eval_grad_f_grad_g_prod(crvec x, crvec y, rvec grad_f, rvec grad_gxy) const override { py::gil_scoped_acquire acq; PYBIND11_OVERRIDE(void, ProblemBase, eval_grad_f_grad_g_prod, x, y, grad_f, grad_gxy); }
    real_t eval_ψ_ŷ(crvec x, crvec y, crvec Σ, rvec ŷ) const override { py::gil_scoped_acquire acq; PYBIND11_OVERRIDE(real_t, ProblemBase, eval_ψ_ŷ, x, y, Σ, ŷ); }
    void eval_grad_ψ_from_ŷ(crvec x, crvec ŷ, rvec grad_ψ, rvec work_n) const override { py::gil_scoped_acquire acq; PYBIND11_OVERRIDE(void, ProblemBase, eval_grad_ψ_from_ŷ, x, ŷ, grad_ψ, work_n); }
    void eval_grad_ψ(crvec x, crvec y, crvec Σ, rvec grad_ψ, rvec work_n, rvec work_m) const override { py::gil_scoped_acquire acq; PYBIND11_OVERRIDE(void, ProblemBase, eval_grad_ψ, x, y, Σ, grad_ψ, work_n, work_m); }
    real_t eval_ψ_grad_ψ(crvec x, crvec y, crvec Σ, rvec grad_ψ, rvec work_n, rvec work_m) const override { py::gil_scoped_acquire acq; PYBIND11_OVERRIDE(real_t, ProblemBase, eval_ψ_grad_ψ, x, y, Σ, grad_ψ, work_n, work_m); }
    // clang-format on
};
